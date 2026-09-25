



creating_queries = """
// ------------------------------------------------------------
// 1. Создание покупателей
// ------------------------------------------------------------

CREATE
(c1:Customer {
    customerId: 1,
    surname: 'Иванов',
    address: 'ул. Ленина, 10'
}),
(c2:Customer {
    customerId: 2,
    surname: 'Петров',
    address: 'ул. Мира, 5'
}),
(c3:Customer {
    customerId: 3,
    surname: 'Сидоров',
    address: 'пр. Победы, 12'
}),
(c4:Customer {
    customerId: 4,
    surname: 'Смирнов',
    address: 'ул. Садовая, 7'
}),
(c5:Customer {
    customerId: 5,
    surname: 'Кузнецов',
    address: 'ул. Центральная, 15'
}),
(c6:Customer {
    customerId: 6,
    surname: 'Попов',
    address: 'ул. Лесная, 3'
}),
(c7:Customer {
    customerId: 7,
    surname: 'Васильев',
    address: 'пр. Северный, 20'
});


// ------------------------------------------------------------
// 2. Создание цехов
// ------------------------------------------------------------

CREATE
(w1:Workshop {
    workshopId: 1,
    name: 'Кухонный цех',
    specialization: 'Кухонная мебель'
}),
(w2:Workshop {
    workshopId: 2,
    name: 'Спальный цех',
    specialization: 'Мебель для спален'
}),
(w3:Workshop {
    workshopId: 3,
    name: 'Гостиный цех',
    specialization: 'Мебель для гостиных'
}),
(w4:Workshop {
    workshopId: 4,
    name: 'Детский цех',
    specialization: 'Детская мебель'
}),
(w5:Workshop {
    workshopId: 5,
    name: 'Столярный цех',
    specialization: 'Столы и стулья'
}),
(w6:Workshop {
    workshopId: 6,
    name: 'Корпусный цех',
    specialization: 'Шкафы и комоды'
}),
(w7:Workshop {
    workshopId: 7,
    name: 'Мягкий цех',
    specialization: 'Диваны и кресла'
});


// ------------------------------------------------------------
// 3. Создание сборщиков
// ------------------------------------------------------------

CREATE
(a1:Assembler {
    assemblerId: 1,
    surname: 'Орлов',
    experience: 8
}),
(a2:Assembler {
    assemblerId: 2,
    surname: 'Соколов',
    experience: 5
}),
(a3:Assembler {
    assemblerId: 3,
    surname: 'Морозов',
    experience: 12
}),
(a4:Assembler {
    assemblerId: 4,
    surname: 'Волков',
    experience: 4
}),
(a5:Assembler {
    assemblerId: 5,
    surname: 'Лебедев',
    experience: 7
}),
(a6:Assembler {
    assemblerId: 6,
    surname: 'Новиков',
    experience: 3
}),
(a7:Assembler {
    assemblerId: 7,
    surname: 'Федоров',
    experience: 10
});


// ------------------------------------------------------------
// 4. Создание мебели
// ------------------------------------------------------------

CREATE
(f1:Furniture {
    furnitureId: 1,
    name: 'Кухонный гарнитур',
    type: 'Кухонная',
    price: 85000
}),
(f2:Furniture {
    furnitureId: 2,
    name: 'Двуспальная кровать',
    type: 'Спальня',
    price: 45000
}),
(f3:Furniture {
    furnitureId: 3,
    name: 'Диван',
    type: 'Гостиная',
    price: 60000
}),
(f4:Furniture {
    furnitureId: 4,
    name: 'Детская кровать',
    type: 'Детская',
    price: 30000
}),
(f5:Furniture {
    furnitureId: 5,
    name: 'Обеденный стол',
    type: 'Кухонная',
    price: 25000
}),
(f6:Furniture {
    furnitureId: 6,
    name: 'Шкаф',
    type: 'Спальня',
    price: 40000
}),
(f7:Furniture {
    furnitureId: 7,
    name: 'Кресло',
    type: 'Гостиная',
    price: 20000
}),
(f8:Furniture {
    furnitureId: 8,
    name: 'Комод',
    type: 'Спальня',
    price: 28000
});


// ------------------------------------------------------------
// 5. Создание заказов
// ------------------------------------------------------------

CREATE
(o1:Order {
    orderId: 1,
    orderDate: date('2026-01-10'),
    completionDate: date('2026-01-20')
}),
(o2:Order {
    orderId: 2,
    orderDate: date('2026-01-15'),
    completionDate: date('2026-01-30')
}),
(o3:Order {
    orderId: 3,
    orderDate: date('2026-02-01'),
    completionDate: date('2026-02-15')
}),
(o4:Order {
    orderId: 4,
    orderDate: date('2026-02-10'),
    completionDate: date('2026-02-28')
}),
(o5:Order {
    orderId: 5,
    orderDate: date('2026-03-01'),
    completionDate: date('2026-03-18')
}),
(o6:Order {
    orderId: 6,
    orderDate: date('2026-03-12'),
    completionDate: date('2026-03-25')
}),
(o7:Order {
    orderId: 7,
    orderDate: date('2026-04-03'),
    completionDate: date('2026-04-20')
});


// ============================================================
// СОЗДАНИЕ СВЯЗЕЙ
// ============================================================

// ------------------------------------------------------------
// 6. Связи покупателей с заказами
// ------------------------------------------------------------

MATCH (c:Customer), (o:Order)
WHERE
    (c.customerId = 1 AND o.orderId = 1) OR
    (c.customerId = 2 AND o.orderId = 2) OR
    (c.customerId = 3 AND o.orderId = 3) OR
    (c.customerId = 1 AND o.orderId = 4) OR
    (c.customerId = 4 AND o.orderId = 5) OR
    (c.customerId = 5 AND o.orderId = 6) OR
    (c.customerId = 6 AND o.orderId = 7)
CREATE (c)-[:MADE]->(o);


// ------------------------------------------------------------
// 7. Связи заказов с мебелью
// В одном заказе может находиться несколько изделий
// ------------------------------------------------------------

MATCH (o:Order), (f:Furniture)
WHERE
    (o.orderId = 1 AND f.furnitureId IN [1, 5]) OR
    (o.orderId = 2 AND f.furnitureId IN [2, 6]) OR
    (o.orderId = 3 AND f.furnitureId = 3) OR
    (o.orderId = 4 AND f.furnitureId = 7) OR
    (o.orderId = 5 AND f.furnitureId = 4) OR
    (o.orderId = 6 AND f.furnitureId = 8) OR
    (o.orderId = 7 AND f.furnitureId = 5)
CREATE (o)-[:CONTAINS]->(f);


// ------------------------------------------------------------
// 8. Связи сборщиков с мебелью
// Один сборщик может собрать несколько изделий
// ------------------------------------------------------------

MATCH (a:Assembler), (f:Furniture)
WHERE
    (a.assemblerId = 1 AND f.furnitureId IN [1, 5]) OR
    (a.assemblerId = 2 AND f.furnitureId = 2) OR
    (a.assemblerId = 3 AND f.furnitureId = 3) OR
    (a.assemblerId = 4 AND f.furnitureId = 4) OR
    (a.assemblerId = 5 AND f.furnitureId = 6) OR
    (a.assemblerId = 6 AND f.furnitureId = 7) OR
    (a.assemblerId = 7 AND f.furnitureId = 8)
CREATE (a)-[:ASSEMBLED]->(f);


// ------------------------------------------------------------
// 9. Связи цехов с производимой мебелью
// ------------------------------------------------------------

MATCH (w:Workshop), (f:Furniture)
WHERE
    (w.workshopId = 1 AND f.furnitureId IN [1, 5]) OR
    (w.workshopId = 2 AND f.furnitureId IN [2, 6, 8]) OR
    (w.workshopId = 3 AND f.furnitureId IN [3, 7]) OR
    (w.workshopId = 4 AND f.furnitureId = 4)
CREATE (w)-[:PRODUCES]->(f);
"""

get_all_nodes = """
// Просмотр всех узлов базы данных
MATCH (n)
RETURN n;
"""

get_graph = """
MATCH (n)-[r]->(m)
RETURN n, r, m;
"""

get_all_customer = """
MATCH (c:Customer)
RETURN c;
"""

get_all_furniture = """
MATCH (f:Furniture)
RETURN f;
"""

get_all_customer_and_orders = """
MATCH (c:Customer)-[m:MADE]->(o:Order)
RETURN c, o, m;
"""

get_furniture_of_orders = """
MATCH (o:Order)-[c:CONTAINS]->(f:Furniture)
RETURN o, f, c;
"""

get_furniture_ordered_by_ivanov = """
MATCH (c:Customer {surname: 'Иванов'})
      -[:MADE]->(o:Order)
      -[:CONTAINS]->(f:Furniture)
RETURN
    c.surname AS customer,
    o.orderId AS orderId,
    f.name AS furniture,
    f.price AS price;
"""

get_sum_orders = """
MATCH (c:Customer)-[:MADE]->(o:Order)-[:CONTAINS]->(f:Furniture)
RETURN
    o.orderId AS orderId,
    c.surname AS customer,
    sum(f.price) AS totalPrice
ORDER BY totalPrice DESC;
"""

get_assemblers_gt_1_furniture = """
MATCH (a:Assembler)-[:ASSEMBLED]->(f:Furniture)
WITH a, count(f) AS furnitureCount
WHERE furnitureCount > 1
RETURN
    a.surname AS assembler,
    furnitureCount;
"""

get_count_furniture_by_workshop = """
MATCH (w:Workshop)
OPTIONAL MATCH (w)-[:PRODUCES]->(f:Furniture)
RETURN
    w.name AS workshop,
    count(f) AS furnitureCount
ORDER BY furnitureCount DESC;
"""

get_biggest_order = """
MATCH (c:Customer)-[:MADE]->(o:Order)-[:CONTAINS]->(f:Furniture)
WITH c, o, sum(f.price) AS totalPrice
RETURN
    o.orderId AS orderId,
    c.surname AS customer,
    totalPrice
ORDER BY totalPrice DESC
LIMIT 1;
"""

get_full_info = """
MATCH (w:Workshop)-[:PRODUCES]->(f:Furniture)<-[:ASSEMBLED]-(a:Assembler)
MATCH (f)<-[:CONTAINS]-(o:Order)<-[:MADE]-(c:Customer)
RETURN
    w.name AS workshop,
    f.name AS furniture,
    a.surname AS assembler,
    o.orderId AS orderId,
    c.surname AS customer
ORDER BY orderId;
"""
