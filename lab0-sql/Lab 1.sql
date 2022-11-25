show tables;
describe jbdebit;
SELECT 
    *
FROM
    jbemployee;
SELECT 
    name
FROM
    jbdept
ORDER BY name;
SELECT 
    name
FROM
    jbparts
WHERE
    qoh = 0;
SELECT 
    name
FROM
    jbemployee
WHERE
    salary >= 9000 AND salary <= 10000;
SELECT 
    name, startyear - birthyear AS start_age
FROM
    jbemployee;
SELECT 
    name
FROM
    jbemployee
WHERE
    name LIKE '%son,%';
SELECT 
    name
FROM
    jbitem
WHERE
    supplier IN (SELECT 
            id
        FROM
            jbsupplier
        WHERE
            name = 'Fisher-Price');
SELECT 
    jbitem.name AS item_name, jbsupplier.name AS supplier_name
FROM
    jbitem
        JOIN
    jbsupplier ON jbitem.supplier = jbsupplier.id
WHERE
    jbsupplier.name = 'Fisher-Price';
SELECT 
    name
FROM
    jbcity
WHERE
    id IN (SELECT 
            city
        FROM
            jbsupplier);
SELECT 
    name, color
FROM
    jbparts
WHERE
    weight > (SELECT 
            weight
        FROM
            jbparts
        WHERE
            name = 'card reader');
SELECT 
    cond1.name, cond1.color
FROM
    jbparts AS cond1,
    jbparts AS cond2
WHERE
    cond2.name = 'card reader'
        AND cond1.weight > cond2.weight;

SELECT 
    AVG(weight) AS 'AvgWeights_black_Parts'
FROM
    jbparts
WHERE
    color = 'black';
SELECT 
    jbsupplier.name AS Supplier_Name,
    SUM(weight * quan) AS SumTotal_weight
FROM
    jbsupplier
        JOIN
    jbcity ON jbsupplier.city = jbcity.id
        JOIN
    jbsupply ON jbsupplier.id = jbsupply.supplier
        JOIN
    jbparts ON jbparts.id = jbsupply.part
WHERE
    state = 'Mass'
GROUP BY jbsupplier.name;
CREATE TABLE jbnewTableItem AS SELECT * FROM
    jbitem
WHERE
    price < (SELECT 
            AVG(price)
        FROM
            jbitem);
ALTER TABLE jbnewTableItem ADD PRIMARY KEY (id);
ALTER TABLE jbnewTableItem ADD FOREIGN KEY (supplier) REFERENCES jbitem(supplier);
SELECT 
    *
FROM
    jbnewtableitem;
