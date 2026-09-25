import os
from collections.abc import Iterable
from typing import Any

from neo4j import Driver, GraphDatabase
from neo4j.graph import Node, Relationship
from prettytable import PrettyTable

from queries import (
    creating_queries,
    get_all_nodes,
    get_graph,
    get_all_customer,
    get_all_furniture,
    get_all_customer_and_orders,
    get_furniture_of_orders,
    get_furniture_ordered_by_ivanov,
    get_sum_orders,
    get_assemblers_gt_1_furniture,
    get_count_furniture_by_workshop,
    get_biggest_order,
    get_full_info,
)


queries = [
    (
        "Просмотр всех узлов базы данных",
        get_all_nodes,
        "table",
    ),
    (
        "Просмотр всего графа со связями",
        get_graph,
        "graph",
    ),
    (
        "Вывести всех покупателей",
        get_all_customer,
        "table",
    ),
    (
        "Вывести всю мебель",
        get_all_furniture,
        "table",
    ),
    (
        "Вывести покупателей и сделанные ими заказы",
        get_all_customer_and_orders,
        "table",
    ),
    (
        "Вывести содержимое каждого заказа",
        get_furniture_of_orders,
        "table",
    ),
    (
        "Вывести все изделия, заказанные покупателем Ивановым",
        get_furniture_ordered_by_ivanov,
        "table",
    ),
    (
        "Рассчитать общую стоимость каждого заказа",
        get_sum_orders,
        "table",
    ),
    (
        "Найти сборщиков, собравших более одного изделия",
        get_assemblers_gt_1_furniture,
        "table",
    ),
    (
        "Вывести количество изделий, произведенных каждым цехом",
        get_count_furniture_by_workshop,
        "table",
    ),
    (
        "Найти самый дорогой заказ",
        get_biggest_order,
        "table",
    ),
    (
        "Вывести полную информацию",
        get_full_info,
        "table",
    ),
]


class Neo4jClient:
    def __init__(
        self,
        uri: str | None = None,
        username: str | None = None,
        password: str | None = None,
        database: str | None = None,
    ) -> None:
        self.uri = uri or os.getenv(
            "NEO4J_URI",
            "neo4j://localhost:7688",
        )
        self.username = username or os.getenv(
            "NEO4J_USERNAME",
            "neo4j",
        )
        self.password = password or os.getenv(
            "NEO4J_PASSWORD",
            "neo4j12345",
        )
        self.database = database or os.getenv(
            "NEO4J_DATABASE",
            "furniture-python",
        )

        self.driver: Driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password),
        )

    def __enter__(self) -> "Neo4jClient":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: Any,
    ) -> None:
        self.close()

    def close(self) -> None:
        self.driver.close()

    def verify_connection(self) -> None:
        self.driver.verify_connectivity()

    def create_database(self) -> None:
        query = f"""
        CREATE DATABASE `{self.database}` IF NOT EXISTS
        """

        self.driver.execute_query(
            query,
            database_="system",
        )

    def execute_query(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
    ):
        return self.driver.execute_query(
            query,
            parameters or {},
            database_=self.database,
        )

    def execute_script(self, script: str) -> None:
        queries = [
            query.strip()
            for query in script.split(";")
            if query.strip()
        ]

        for query in queries:
            self.execute_query(query)

    def is_empty(self) -> bool:
        records, _, _ = self.execute_query(
            """
            MATCH (n)
            RETURN count(n) AS node_count
            """
        )

        return records[0]["node_count"] == 0

    @staticmethod
    def _format_node(node: Node) -> str:
        labels = ":".join(node.labels)
        properties = dict(node)

        display_properties = {
            "Customer": "surname",
            "Assembler": "surname",
            "Workshop": "name",
            "Furniture": "name",
            "Order": "orderId",
        }

        name_property = next(
            (
                property_name
                for label in node.labels
                if (property_name := display_properties.get(label))
                and property_name in properties
            ),
            None,
        )

        if name_property:
            name = str(properties[name_property])

            if "Order" in node.labels:
                name = f"Заказ #{name}"

        else:
            name = str(properties)

        return f"{labels}: {name}"

    @classmethod
    def _format_relationship(
        cls,
        relationship: Relationship,
    ) -> str:
        start = cls._format_node(
            relationship.start_node,
        )
        end = cls._format_node(
            relationship.end_node,
        )

        return (
            f"{start} "
            f"-[:{relationship.type}]-> "
            f"{end}"
        )

    @classmethod
    def _format_value(cls, value: Any) -> str:
        if isinstance(value, Node):
            return cls._format_node(value)

        if isinstance(value, Relationship):
            return cls._format_relationship(value)

        if isinstance(value, list):
            return ", ".join(
                cls._format_value(item)
                for item in value
            )

        if isinstance(value, dict):
            return str(value)

        return str(value)

    @classmethod
    def print_table(
        cls,
        records: Iterable,
        title: str | None = None,
    ) -> None:
        if title:
            print(f"\n{title}")

        records = list(records)

        if not records:
            print("Запрос не вернул результатов.")
            return

        table = PrettyTable()

        table.field_names = list(records[0].keys())

        for record in records:
            table.add_row(
                [
                    cls._format_value(record[key])
                    for key in table.field_names
                ]
            )

        table.align = "l"
        table.max_width = 50

        print(table)

    @classmethod
    def print_graph(
        cls,
        records: Iterable,
        title: str | None = None,
    ) -> None:
        if title:
            print(f"\n{title}")

        records = list(records)

        if not records:
            print("Граф пуст.")
            return

        table = PrettyTable()

        table.field_names = [
            "Откуда",
            "Связь",
            "Куда",
        ]

        for record in records:
            start_node: Node = record["n"]
            relationship: Relationship = record["r"]
            end_node: Node = record["m"]

            table.add_row(
                [
                    cls._format_node(start_node),
                    relationship.type,
                    cls._format_node(end_node),
                ]
            )

        table.align = "l"
        table.max_width = 40

        print(table)


with Neo4jClient() as client:
    client.create_database()
    client.verify_connection()

    if client.is_empty():
        print("БД пустая. Создаём граф...")
        client.execute_script(creating_queries)
    else:
        print("БД уже содержит данные. Создание графа пропущено.")

    for name, query, output_type in queries:
        records, _, _ = client.execute_query(query)

        if output_type == "graph":
            client.print_graph(
                records,
                title=name,
            )
        else:
            client.print_table(
                records,
                title=name,
            )
            