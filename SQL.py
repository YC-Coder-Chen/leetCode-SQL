# 262
"""
SELECT t.Request_at AS "Day", 
        CAST(SUM(CASE 
                WHEN t.Status != 'completed' THEN 1
                ELSE 0
           END) / COUNT(*) AS decimal(16,2)) AS "Cancellation Rate"
FROM Trips t
LEFT JOIN Users u1 on u1.Users_Id =  t.Client_Id
LEFT JOIN Users u2 on u2.Users_Id =  t.Driver_Id
WHERE u1.Banned = 'No' AND u2.Banned = 'No' AND t.Request_at BETWEEN "2013-10-01" AND "2013-10-03"
GROUP BY t.Request_at
;
"""

# 185
"""
SELECT d.Name AS "Department", e.Name AS "Employee", e.Salary
FROM Employee e
JOIN Department d on e.DepartmentId = d.Id
JOIN (
    SELECT e.Name, COUNT(DISTINCT e2.Salary) AS "Rownum"
    FROM Employee e
    JOIN Employee e2 on e.DepartmentId = e2.DepartmentId
    WHERE  e.Salary <= e2.Salary AND e.DepartmentId = e2.DepartmentId
    GROUP BY e.Id ) t on e.Name = t.Name
WHERE t.RowNum <=3
ORDER BY d.Name ASC, e.Salary DESC
;
"""

# 579
"""
SELECT e.Id AS "id", e.Month AS "month", SUM(e2.Salary) AS "Salary"
FROM Employee e
JOIN Employee e2 on e.Id = e2.Id
WHERE e.Month < (SELECT MAX(e3.Month) 
                 FROM Employee e3
                 WHERE e.Id = e3.Id) AND e.Month >= e2.Month 
                                     AND e.Month - 3 < e2.Month
GROUP BY e.Id, e.Month
ORDER BY e.Id ASC, e.Month DESC
;
"""

# 601
"""
SELECT s1.id, s1.visit_date, s1.people
FROM stadium s1
WHERE (SELECT COUNT(*)
       FROM stadium s2
       WHERE s1.id < s2.id + 1 AND s1.id > s2.id - 3 AND s2.people>=100) = 3
       OR
       (SELECT COUNT(*)
       FROM stadium s3
       WHERE s1.id < s3.id + 2 AND s1.id > s3.id - 2 AND s3.people>=100) = 3
       OR
       (SELECT COUNT(*)
       FROM stadium s4
       WHERE s1.id < s4.id + 3 AND s1.id > s4.id - 1 AND s4.people>=100) = 3 
"""


# 615
"""
SELECT t1.pay_month, t1.department_id,             
        (CASE WHEN CAST(t1.avg_salary AS decimal(16,2)) > (SELECT CAST(AVG(s2.amount) AS decimal(16,2))
                                    FROM salary s2
                                    WHERE DATE_FORMAT(s2.pay_date,'%Y-%m') = t1.pay_month) THEN "higher"
              WHEN CAST(t1.avg_salary AS decimal(16,2)) = (SELECT CAST(AVG(s2.amount) AS decimal(16,2))
                                    FROM salary s2
                                    WHERE DATE_FORMAT(s2.pay_date,'%Y-%m') = t1.pay_month) THEN "same"
         ELSE "lower"
         END) AS "comparison"
FROM (
    SELECT DATE_FORMAT(s.pay_date,'%Y-%m') AS "pay_month", 
                e.department_id AS "department_id", AVG(s.amount) AS "avg_salary"
    FROM salary s
    JOIN employee e on s.employee_id = e.employee_id 
    GROUP BY e.department_id, DATE_FORMAT(s.pay_date,'%Y-%m') ) t1
"""


# 618
# use @ function to create row_number()
"""
SELECT Am_table.America, As_table.Asia, Eu_table.Europe
FROM (SELECT @am:=@am+1 AS idx_am, s1.name AS America
      FROM (SELECT @am:=0) c, student s1
      WHERE s1.continent = 'America'
      ORDER BY America ASC) Am_table
LEFT JOIN (
      SELECT @asia:=@asia+1 AS idx_as, s2.name AS Asia
      FROM (SELECT @asia:=0) c, student s2
      WHERE s2.continent = 'Asia'
      ORDER BY Asia ASC) As_table
ON Am_table.idx_am = As_table.idx_as
LEFT JOIN (
      SELECT @eu:=@eu+1 AS idx_eu, s3.name AS Europe
      FROM (SELECT @eu:=0) c, student s3
      WHERE s3.continent = 'Europe'
      ORDER BY Europe ASC) Eu_table
ON Am_table.idx_am = Eu_table.idx_eu
"""

# 1127
"""
SELECT DISTINCT (sp.spend_date), sp3.platform, 
                IFNULL(clean_spending.total_amount,0) AS "total_amount",
                IFNULL(clean_spending.total_users,0) AS "total_users"
FROM Spending sp
CROSS JOIN 
    (SELECT DISTINCT (sp2.platform)
     FROM Spending sp2
     UNION (SELECT 'both' FROM Spending sp3)) sp3
LEFT JOIN 
    (SELECT s.spend_date,
           (CASE WHEN s2.count_platform = 2 THEN "both" ELSE s.platform END) AS "clean_platform",
           SUM(s.amount) AS "total_amount", 
           COUNT(DISTINCT s.user_id) AS "total_users"
    FROM Spending s
    LEFT JOIN (SELECT user_id, spend_date, COUNT(DISTINCT platform) AS count_platform
        FROM Spending
        GROUP BY user_id, spend_date) s2
    ON s.user_id = s2.user_id AND s.spend_date = s2.spend_date
    GROUP BY s.spend_date, clean_platform ) clean_spending
ON sp.spend_date = clean_spending.spend_date AND sp3.platform = clean_spending.clean_platform
ORDER BY CASE sp3.platform WHEN "desktop" THEN 0
                           WHEN "mobile" THEN 1
                           ELSE 2
                           END
"""

# 571
"""
SELECT agg2.Clean_median AS "median"
FROM (SELECT agg.cum_fre, 
           CASE WHEN agg.cum_fre=0.5 THEN (agg.Number + agg.Sub_num)/2
           ELSE agg.Number END AS Clean_median
    FROM (SELECT n1.Number, MIN(n2.Number) AS "Sub_num",
           @fre:=@fre+n1.Frequency/(SELECT SUM(n3.Frequency)
                                    FROM Numbers n3) AS cum_fre
         FROM (SELECT @fre:=0) c, Numbers n1
         LEFT JOIN Numbers n2 on n1.Number < n2.Number 
         GROUP BY n1.Number) agg ) agg2
WHERE agg2.cum_fre >=0.5
ORDER BY agg2.Clean_median
LIMIT 1
"""

# 1159
"""
SELECT DISTINCT u2.user_id AS "seller_id", agg.2nd_item_fav_brand
FROM Users u2
LEFT JOIN (
    SELECT o1.seller_id, CASE WHEN u.favorite_brand = i.item_brand THEN "yes"
                              ELSE "no" END AS "2nd_item_fav_brand"
    FROM Orders o1
    LEFT JOIN Users u on o1.seller_id = u.user_id
    LEFT JOIN Items i on o1.item_id = i.item_id
    WHERE (SELECT COUNT(order_id) FROM Orders o2 
           WHERE o1.seller_id = o2.seller_id 
           AND o1.order_date>o2.order_date) = 1

    ) agg
ON u2.user_id = agg.seller_id
ORDER BY u2.user_id
"""

# 1097
"""
SELECT a.event_date AS "install_dt",
       COUNT(DISTINCT a.player_id) AS "installs", 
       CAST(AVG(CASE WHEN a3.games_played>0 THEN 1
           ELSE 0 END) AS decimal(16,2)) AS "Day1_retention"
FROM ((SELECT a2.player_id, MIN(a2.event_date) AS "event_date"
       FROM Activity a2
       GROUP BY a2.player_id)) a
LEFT JOIN Activity a3 
ON a3.player_id = a.player_id AND a3.event_date = DATE_ADD(a.event_date, INTERVAL 1 DAY)             
GROUP BY a.event_date
"""

# 569
"""
SELECT clean.Id, clean.Company , clean.Salary
FROM (
    SELECT e.Id, e.Company, e.Salary, (
           SELECT SUM( CASE WHEN e2.Salary <= e.Salary AND e2.Id < e.Id THEN 1
                            WHEN e2.Salary < e.Salary THEN 1
                            ELSE 0 END) 
           FROM Employee e2
           WHERE e2.Company = e.Company AND e2.Salary <= e.Salary ) AS "small", 
           (SELECT SUM( CASE WHEN e3.Salary >= e.Salary AND e3.Id > e.Id THEN 1
                             WHEN e3.Salary > e.Salary THEN 1
                             ELSE 0 END) 
           FROM Employee e3
           WHERE e3.Company = e.Company AND e3.Salary >= e.Salary ) AS "large"
    FROM Employee e ) clean
WHERE ABS(clean.small - clean.large) <= 1 
ORDER BY clean.Company, clean.Salary
"""

# below is faster
"""
SELECT clean.Id, clean.Company, clean.Salary
FROM (
    SELECT e.Id, e.Company, e.Salary, (
               SELECT SUM( CASE WHEN e2.Salary <= e.Salary AND e2.Id < e.Id THEN 1
                                WHEN e2.Salary < e.Salary THEN 1
                                ELSE 0 END) + 1
               FROM Employee e2
               WHERE e2.Company = e.Company AND e2.Salary <= e.Salary ) AS "small",
               e4.sum_count
    FROM Employee e
    LEFT JOIN (SELECT e3.Company, COUNT(*) AS "sum_count"
               FROM Employee e3
               GROUP BY e3.Company) e4
    ON e.Company = e4.Company ) clean
WHERE ABS((clean.sum_count + 1)/2 - clean.small) <= 0.5
ORDER BY clean.Company, clean.Salary
"""

# 1194
"""
SELECT group_max.group_id AS "GROUP_ID", clean2.player_id AS "PLAYER_ID"
FROM (
    SELECT clean.group_id, MAX(clean.total_score) AS "max_score"
    FROM (
        SELECT p.player_id, p.group_id, 
               SUM(IFNULL(m.first_score, 0)) AS "total_score"
        FROM Players p
        LEFT JOIN (SELECT m.first_player, m.first_score
                   FROM Matches m
                   UNION ALL (SELECT m2.second_player, m2.second_score
                          FROM Matches m2)) m
        ON p.player_id = m.first_player
        GROUP BY p.player_id, p.group_id) clean
    GROUP BY clean.group_id) group_max
JOIN (
    SELECT p.player_id, p.group_id, 
           SUM(IFNULL(m.first_score, 0)) AS "total_score"
    FROM Players p
    LEFT JOIN (SELECT m.first_player, m.first_score
               FROM Matches m
               UNION ALL(SELECT m2.second_player, m2.second_score
                      FROM Matches m2)) m
    ON p.player_id = m.first_player
    GROUP BY p.player_id, p.group_id) clean2
ON group_max.max_score = clean2.total_score AND group_max.group_id = clean2.group_id
WHERE clean2.player_id = (SELECT MIN(clean3.player_id)
                         FROM (
                                SELECT p.player_id, p.group_id, 
                                       SUM(IFNULL(m.first_score, 0)) AS "total_score"
                                FROM Players p
                                LEFT JOIN (SELECT m.first_player, m.first_score
                                           FROM Matches m
                                           UNION ALL(SELECT m2.second_player, m2.second_score
                                                  FROM Matches m2)) m
                                ON p.player_id = m.first_player
                                GROUP BY p.player_id, p.group_id) clean3
                         WHERE clean3.total_score = group_max.max_score AND clean3.group_id = clean2.group_id)
ORDER BY group_max.group_id
"""

# 614
"""
SELECT DISTINCT f.follower, f3.num
FROM follow f 
JOIN (SELECT f2.followee, COUNT(DISTINCT f2.follower) AS "num"
      FROM follow f2
      GROUP BY f2.followee) f3
ON f.follower = f3.followee
ORDER BY f.follower
"""

# 117
"""
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
  RETURN (
      SELECT clean.Salary
      FROM (SELECT e.Salary, (SELECT COUNT(DISTINCT e2.Salary) + 1
                              FROM Employee e2
                              WHERE e2.Salary < e.Salary) AS "nth"
            FROM Employee e ) clean
      WHERE clean.nth = N
      LIMIT 1
      
  );
END
"""
# faster
"""
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN

DECLARE row_start INT;
SET row_start = N - 1;

  RETURN (
      SELECT DISTINCT e.Salary
      FROM Employee e
      ORDER BY e.Salary DESC
      LIMIT 1 OFFSET row_start
      
  );
END
"""

# 184
"""
SELECT d.Name AS "Department", e.Name AS "Employee", e.Salary
FROM Employee e
JOIN Department d ON e.DepartmentId = d.Id
WHERE (SELECT COUNT(DISTINCT e2.Id)
       FROM Employee e2
       WHERE e2.Salary > e.Salary AND e2.DepartmentId  = e.DepartmentId ) = 0
"""
# faster
"""
SELECT d.Name AS "Department", e.Name AS "Employee", e.Salary
FROM Employee e
JOIN Department d ON e.DepartmentId = d.Id
WHERE (e.DepartmentId, e.Salary) IN
      ( SELECT e2.DepartmentId, MAX(e2.Salary)
        FROM Employee e2
        GROUP BY e2.DepartmentId
      )
"""

# 1132
"""
SELECT ROUND(AVG(clean.daily) * 100, 2) AS "average_daily_percent"
FROM (
    SELECT a.action_date, COUNT(DISTINCT CASE WHEN r.remove_date IS NOT NULL THEN a.post_id END)/COUNT(DISTINCT a.post_id) AS "daily"
    FROM Actions a 
    LEFT JOIN Removals r
    ON a.post_id = r.post_id
    WHERE a.extra = "spam"
    GROUP BY a.action_date ) clean
"""

# 180
"""
SELECT DISTINCT l.Num AS "ConsecutiveNums"
FROM Logs l
JOIN Logs l2
ON l.Id + 1 = l2.Id
JOIN Logs l3
ON l2.Id + 1 = l3.Id
WHERE l.Num = l2.Num AND l2.Num = l3.Num
ORDER BY l.NUm ASC
"""

# 578
"""
SELECT clean.question_id AS "survey_log"
FROM (
    SELECT s.question_id, 
           SUM(CASE WHEN action = "answer" THEN 1 END)/
           SUM(CASE WHEN action = "show" THEN 1 END) AS "answer_rate"
    FROM survey_log s
    GROUP BY s.question_id) clean
ORDER BY clean.answer_rate DESC
LIMIT 1
"""

# 574
"""
SELECT c.Name
FROM (
    SELECT clean_vote.CandidateId
    FROM (
        SELECT v.CandidateId, COUNT(v.CandidateId) AS "num_vote"
        FROM Vote v
        GROUP BY v.CandidateId) clean_vote
    ORDER BY clean_vote.num_vote DESC
    LIMIT 1 ) clean2
JOIN Candidate c
ON clean2.CandidateId = c.id
"""

# 178
"""
SELECT s.Score, 
       (SELECT COUNT(DISTINCT s2.Score)
        FROM Scores s2
        WHERE s2.Score > s.Score) + 1 AS "Rank"
FROM Scores s
ORDER BY s.Score DESC
"""

# 1098
"""
SELECT b2.book_id, b2.name
FROM Books b2
LEFT JOIN (
    SELECT o.book_id, b.name, SUM(quantity) AS "num_sold"
    FROM Orders o
    LEFT JOIN Books b
    ON o.book_id = b.book_id
    WHERE o.dispatch_date BETWEEN DATE_SUB('2019-06-23', INTERVAL 1 YEAR) AND '2019-06-23'
    GROUP BY o.book_id ) sold
ON b2.book_id = sold.book_id
WHERE b2.available_from < DATE_SUB('2019-06-23', INTERVAL 1 MONTH)
AND IFNULL(sold.num_sold, 0) < 10
"""

# 1107
"""
SELECT first_login.login_date, COUNT(DISTINCT first_login.user_id) AS "user_count"
FROM (
    SELECT t.user_id, MIN(t.activity_date) AS "login_date"
    FROM Traffic t
    WHERE t.activity = "login"
    GROUP BY t.user_id) first_login
WHERE first_login.login_date BETWEEN DATE_SUB("2019-06-30", INTERVAL 90 DAY) 
AND "2019-06-30"
GROUP BY first_login.login_date
"""

# 550
"""
SELECT ROUND(COUNT(DISTINCT CASE WHEN a2.event_date IS NOT NULL THEN a.player_id END)/ COUNT(DISTINCT a.player_id),2) AS "fraction"
FROM Activity a
LEFT JOIN Activity a2
ON DATE_ADD(a.event_date, INTERVAL 1 DAY) = a2.event_date  AND a.player_id = a2.player_id
JOIN (SELECT a3.player_id, MIN(a3.event_date) AS "start_date"
      FROM Activity a3
      GROUP BY a3.player_id
      ) start_date_table
ON a.event_date = start_date_table.start_date AND a.player_id = start_date_table.player_id
"""

# 580
"""
SELECT d.dept_name, COUNT(DISTINCT s.student_id) AS "student_number"
FROM department d
LEFT JOIN student s
ON d.dept_id = s.dept_id
GROUP BY d.dept_name
ORDER BY student_number DESC, d.dept_name
"""

# 1070
"""
SELECT s2.product_id, s2.year AS "first_year", s2.quantity, s2.price
FROM Sales s2
JOIN (
    SELECT s.product_id, MIN(s.year) AS "year"
    FROM Sales s
    GROUP BY s.product_id ) first_year
ON s2.product_id = first_year.product_id AND s2.year = first_year.year
"""

# 602
"""
SELECT union_table.requester_id AS "id", COUNT(*) AS "num"
FROM (
    SELECT r.requester_id
    FROM request_accepted r
    UNION ALL (SELECT r2.accepter_id
           FROM request_accepted r2)) union_table
GROUP BY union_table.requester_id
ORDER BY num DESC
LIMIT 1
"""

# 1149
"""
SELECT DISTINCT count_views.viewer_id AS "id"
FROM (
    SELECT v.viewer_id, v.view_date, COUNT(DISTINCT v.article_id) AS "views"
    FROM Views v
    GROUP BY v.viewer_id, v.view_date) count_views
WHERE count_views.views >= 2
"""

# 585
"""
SELECT ROUND(SUM(distinct_table.TIV_2016),2) AS "TIV_2016"
FROM (
    SELECT DISTINCT i.PID, i.TIV_2016, i3.LAT AS "LAT"
    FROM insurance i
    JOIN insurance i2 ON i.TIV_2015 = i2.TIV_2015 AND i.PID != i2.PID
    LEFT JOIN insurance i3 ON i.LAT = i3.LAT AND i.LON = i3.LON AND i.PID != i3.PID
    ) distinct_table
WHERE distinct_table.LAT IS NULL
"""

# 585 takes longer time but more clear
"""
SELECT ROUND(SUM(condition_table.TIV_2016),2) AS "TIV_2016"
FROM (
    SELECT i.PID, i.TIV_2016,
           (SELECT COUNT(DISTINCT i2.PID) 
            FROM insurance i2
            WHERE i2.TIV_2015=i.TIV_2015 AND i2.PID!=i.PID) AS "first_req",
           (SELECT COUNT(DISTINCT i3.PID) 
            FROM insurance i3
            WHERE i3.LAT=i.LAT AND i3.LON=i.LON AND i3.PID!=i.PID) AS "second_req"   
    FROM  insurance i ) condition_table
WHERE condition_table.first_req !=0 AND condition_table.second_req = 0
"""
# 1205
"""
SELECT union_table.month, union_table.country, 
       SUM(CASE WHEN union_table.state = "approved" THEN 1 ELSE 0 END)
       AS "approved_count",
       SUM(CASE WHEN union_table.state = "approved" THEN union_table.amount ELSE 0 END)
       AS "approved_amount",    
       SUM(CASE WHEN union_table.state = "Chargebacks" THEN 1 ELSE 0 END) AS "chargeback_count",
       SUM(CASE WHEN union_table.state = "Chargebacks" THEN union_table.amount ELSE 0 END)
       AS "chargeback_amount"       
FROM (
    SELECT c.trans_id, t.country, "Chargebacks" AS "state", t.amount, DATE_FORMAT(c.trans_date, "%Y-%m") AS "month"
    FROM Chargebacks c
    LEFT JOIN Transactions t on t.id = c.trans_id
    UNION (SELECT t2.id, t2.country, t2.state, t2.amount, 
           DATE_FORMAT(t2.trans_date, "%Y-%m") AS "month"
           FROM Transactions t2)) union_table
GROUP BY union_table.month, union_table.country
HAVING approved_count + approved_amount + chargeback_count + chargeback_amount > 0
"""

# 1158
"""
SELECT u.user_id AS "buyer_id", u.join_date, IFNULL(clean_orders.orders_in_2019, 0) AS "orders_in_2019"
FROM Users u
LEFT JOIN (SELECT o.buyer_id, COUNT(DISTINCT order_id) AS 'orders_in_2019'
           FROM Orders o
           WHERE YEAR(o.order_date) = 2019
           GROUP BY o.buyer_id) clean_orders
ON u.user_id = clean_orders.buyer_id
"""

# 1174
"""
SELECT ROUND(COUNT(DISTINCT CASE WHEN first_table.first_date = d2.customer_pref_delivery_date THEN d2.customer_id END)/COUNT(DISTINCT d2.customer_id) * 100,2) AS "immediate_percentage"
FROM (
    SELECT d.customer_id, MIN(d.order_date) AS "first_date"
    FROM Delivery d
    GROUP BY d.customer_id) first_table
LEFT JOIN Delivery d2
ON d2.customer_id = first_table.customer_id AND d2.order_date = first_table.first_date
"""

# 1174 
# faster, using IN is faster than the previous one
"""
SELECT ROUND(COUNT(DISTINCT CASE WHEN d.order_date = d.customer_pref_delivery_date THEN d.customer_id END)/COUNT(DISTINCT d.customer_id) * 100,2) AS "immediate_percentage"
FROM Delivery d
WHERE (d.customer_id, d.order_date) IN (SELECT d2.customer_id, MIN(d2.order_date)
									    FROM delivery d2
									    GROUP BY d2.customer_id)
"""

# 612
# no aggregate function allowed during features created by select
"""
SELECT ROUND((SELECT MIN(SQRT(POWER(p.x-p2.x,2) + POWER(p.y-p2.y,2)))
        FROM point_2d p2
        WHERE p.x != p2.x OR p.y!=p2.y),2) AS "shortest"
FROM point_2d p
ORDER BY shortest ASC
LIMIT 1
"""

# 626
"""
SELECT s.id, IFNULL(CASE WHEN MOD(s.id,2) = 1 THEN s2.student
                  WHEN MOD(s.id,2) = 0 THEN s3.student
                  END, s.student) AS "student" 
FROM seat s
LEFT JOIN seat s2 on s.id + 1 = s2.id 
LEFT JOIN seat s3 on s.id - 1 = s3.id
ORDER BY s.id ASC
"""

# 1193
"""
SELECT DATE_FORMAT(t.trans_date, "%Y-%m") AS "month", t.country, 
       COUNT(DISTINCT t.id) AS "trans_count",
       COUNT(DISTINCT CASE WHEN t.state = "approved" THEN t.id END) AS "approved_count",
       SUM(t.amount) AS "trans_total_amount",
       SUM(CASE WHEN t.state = "approved" THEN t.amount ELSE 0 END) AS "approved_total_amount"
FROM Transactions t
GROUP BY DATE_FORMAT(t.trans_date, "%Y-%m"), t.country
"""

# 1212
"""
SELECT t.team_id, t.team_name, IFNULL(SUM(clean_score.host_score),0) AS "num_points"
FROM Teams t
LEFT JOIN (
    SELECT host_table.*
    FROM (SELECT m.host_team, m.guest_team,
          (CASE WHEN m.host_goals > m.guest_goals THEN 3
                WHEN m.host_goals = m.guest_goals THEN 1
                ELSE 0 END) AS "host_score"
          FROM Matches m) host_table
    UNION ALL
    (SELECT m2.guest_team, m2.host_team,
           (CASE WHEN m2.host_goals < m2.guest_goals THEN 3
                 WHEN m2.host_goals = m2.guest_goals THEN 1
                 ELSE 0 END) AS "guest_score"
            FROM Matches m2)) clean_score 
ON t.team_id = clean_score.host_team
GROUP BY t.team_id
ORDER BY num_points DESC, team_id ASC
"""

# 1164
"""
SELECT DISTINCT p3.product_id, IFNULL(price_table.price, 10) AS "price"
FROM Products p3
LEFT JOIN (
    SELECT p.product_id, p.new_price AS "price"
    FROM Products p
    WHERE (p.product_id, p.change_date) IN 
        (SELECT p2.product_id, MAX(p2.change_date) AS "change_date"
         FROM Products p2
         WHERE p2.change_date <= '2019-08-16'
         GROUP BY p2.product_id
         )
    ) price_table
ON p3.product_id = price_table.product_id
ORDER BY price DESC
"""

# 608
"""
SELECT count_table.id, (CASE WHEN count_table.p_id IS NULL THEN "Root"
                  WHEN count_table.parent_count = 0 THEN "Leaf"
                  ELSE "Inner" END) AS "Type"
FROM (
    SELECT t.id, t.p_id, (SELECT COUNT(t2.p_id)
                    FROM tree t2
                    WHERE t2.p_id = t.id) AS 'parent_count'
    FROM tree t ) count_table
"""

# 608 
# using join is faster
"""
SELECT t2.id , (CASE WHEN t2.p_id IS NULL THEN "Root"
                   WHEN parent_table.parent_count IS NULL THEN "Leaf"
                   ELSE 'Inner' END) AS "Type"
                   
FROM tree t2
LEFT JOIN (
    SELECT t.p_id, COUNT(t.p_id) AS "parent_count"
    FROM tree t
    WHERE t.p_id IS NOT NULL
    GROUP BY t.p_id) parent_table
ON t2.id = parent_table.p_id
"""

# 1112
"""
SELECT e2.student_id, MIN(e2.course_id) AS "course_id", e2.grade
FROM Enrollments e2
WHERE (e2.student_id, e2.grade) IN (SELECT e.student_id, MAX(e.grade) AS "grade"
                                    FROM Enrollments e
                                    GROUP BY e.student_id)
GROUP BY e2.student_id
"""

# 570
"""
SELECT e2.Name
FROM Employee e2
JOIN (
    SELECT e.ManagerId, COUNT(DISTINCT e.Id) AS "num_reporters"
    FROM Employee e
    GROUP BY e.ManagerId 
    HAVING num_reporters >= 5) reporters_table
ON e2.Id = reporters_table.ManagerId
"""

# 534
"""
SELECT a.player_id, a.event_date, (SELECT SUM(games_played)
                                                FROM Activity a2
                                                WHERE a2.player_id = a.player_id AND a2.event_date <= a.event_date) AS "games_played_so_far"
FROM Activity a
"""

# 534
# faster
"""
SELECT a.player_id, a.event_date, SUM(a2.games_played) AS "games_played_so_far"
FROM Activity a, Activity a2
WHERE a.player_id = a2.player_id AND a.event_date >= a2.event_date
GROUP BY a.player_id, a.event_date
"""


