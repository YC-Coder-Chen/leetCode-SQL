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

# 579 Echo
# Putting the and conditions in 'ON Clause' will be much slower
"""
SELECT E.Id AS 'id', E.Month AS 'month', SUM(IFNULL(E1.Salary,0)) AS 'Salary'
FROM Employee E
lEFT JOIN Employee E1
ON E.Id = E1.Id and E1.Month+2 >= E.Month and E.Month >= E1.Month
WHERE (E.Id, E.Month) NOT IN
    (SELECT Id, MAX(Month) AS 'last_month'
    FROM Employee
    GROUP BY Id) 
GROUP BY E.Id, E.Month
ORDER BY E.Id ASC, E.Month DESC
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

# 601 Echo
"""
SELECT S.id,S.visit_date,S.people
FROM stadium S
LEFT JOIN (SELECT id,visit_date,people,IF(people>=100,1,0) AS 'check'
FROM stadium) AS A
ON S.id+2 = A.id
LEFT JOIN (SELECT id,visit_date,people,IF(people>=100,1,0) AS 'check'
FROM stadium) AS B
ON S.id+1 = B.id
lEFT JOIN (SELECT id,visit_date,people,IF(people>=100,1,0) AS 'check'
FROM stadium) AS C
ON S.id-1 = C.id
LEFT JOIN (SELECT id,visit_date,people,IF(people>=100,1,0) AS 'check'
FROM stadium) AS D
ON S.id-2 = D.id
WHERE ((S.people>=100) and A.check=1 and B.check=1)
      OR ((S.people>=100) and B.check=1 and C.check=1)
      OR ((S.people>=100) and C.check=1 and D.check=1)
ORDER BY id
"""

# 601 Answer from wangyihuan24 https://leetcode.com/wanyihuang24/
"""
SELECT DISTINCT S1.*
FROM stadium S1
JOIN stadium S2
JOIN stadium S3
ON ((S1.id = S2.id - 1 AND S1.id = S3.id -2)
OR (S3.id = S1.id - 1 AND S3.id = S2.id -2)
OR (S3.id = S2.id - 1 AND S3.id = S1.id -2))
WHERE S1.people >= 100
AND S2.people >= 100
AND S3.people >= 100
ORDER BY S1.id;
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

# 615 Echo
"""
SELECT date_format(S.pay_date,'%Y-%m') AS 'pay_month',
       E.department_id,
      ( CASE WHEN ROUND(AVG(S.amount),2)> A.avg THEN 'higher'
             WHEN ROUND(AVG(S.amount),2)= A.avg THEN 'same'
             ELSE 'lower' END) AS 'comparison'
FROM salary S
lEFT JOIN (SELECT date_format(pay_date,'%Y-%m') AS 'month',
           ROUND(AVG(amount),2) AS 'avg' 
           FROM Salary
           GROUP BY date_format(pay_date,'%Y-%m')) AS A
ON date_format(S.pay_date,'%Y-%m') = A.month
LEFT JOIN employee E
ON S.employee_id = E.employee_id
GROUP BY date_format(S.pay_date,'%Y-%m'), E.department_id
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

# 1127 Echo
"""
SELECT D.spend_date,D.platform,IFNULL(S2.total_amount,0) AS 'total_amount',
       IFNULL(S2.total_users,0) AS 'total_users'
FROM
(SELECT * FROM
    (SELECT DISTINCT spend_date FROM Spending) AS A
    JOIN 
    (SELECT 'desktop' AS 'platform'
    UNION
    SELECT 'mobile' AS 'platform'
    UNION 
    SELECT 'both' AS 'platform') AS P
    ON 1) AS D
lEFT JOIN 
(SELECT S1.spend_date,S1.platform,
       SUM(S1.t_amount) AS 'total_amount',
       COUNT(S1.user_id) AS 'total_users'
FROM 
       (SELECT S.user_id, S.spend_date,
               SUM(S.amount) AS 't_amount',
               (CASE WHEN COUNT(S.platform)=2 THEN 'both'
                ELSE S.platform END) AS 'platform'
        FROM Spending S
        GROUP BY user_id, spend_date) AS S1
GROUP BY S1.spend_date, S1.platform) AS S2
ON D.platform = S2.platform and D.spend_date = S2.spend_date
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

# 571 Echo
"""
SELECT AVG(Number) 'median'
FROM
    (SELECT Number, Frequency, @cum:=@cum+Frequency AS 'cum'
    FROM Numbers, (SELECT @cum:=0) tmp
    ORDER BY Number) AS N_cum
WHERE 
    ((SELECT ROUND(SUM(Frequency)/2,0) FROM Numbers) 
        between cum-Frequency+1 and cum)
    OR ((SELECT ROUND(SUM(Frequency)/2+0.5,0) FROM Numbers)
        between cum-Frequency+1 and cum)
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
 
# 1159 faster if getting rank first. answer from ying61 https://leetcode.com/ying61/
"""
select u.user_id seller_id, case when u.favorite_brand = i.item_brand then "yes" else "no" end 2nd_item_fav_brand
from Users u 
left outer join
(select seller_id, order_date, item_id,
       # assume Orders table is in chronological order
       case when @prev = seller_id then @rank := @rank + 1 else @rank := 1 end Rank,
       @prev := seller_id partition_key
FROM Orders
join (select @rank := 0, @prev := 0) tmp
order by seller_id, order_date asc) rt
on u.user_id = rt.seller_id and rt.Rank = 2
left outer join Items i
on rt.item_id = i.item_id
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

# 1097 Echo
"""
SELECT Install.install_dt, Install.installs, 
       ROUND(IFNULL(Re.retention/Install.installs,0),2) As 'Day1_retention'
FROM 
    (SELECT  install_dt, COUNT(*) AS 'installs'
    FROM Activity A
    LEFT JOIN 
        (SELECT player_id,min(event_date) AS 'install_dt'
        FROM Activity
        GROUP BY player_id) AS install_table
    ON A.player_id = install_table.player_id 
    WHERE A.event_date = install_table.install_dt
    GROUP BY install_dt) AS Install    
LEFT JOIN
    (SELECT install_dt,
           COUNT(*) AS 'retention'
    FROM Activity A2
    LEFT JOIN (SELECT player_id,min(event_date) AS 'install_dt'
        FROM Activity
        GROUP BY player_id) AS install_table
    ON A2.player_id = install_table.player_id 
    WHERE A2.event_date = adddate(install_dt,interval 1 day)
    GROUP BY install_dt) AS Re
ON Re.install_dt = Install.install_dt
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

# 569 Echo beats 99%
"""
SELECT Id, Company, Salary
FROM
    (SELECT Id, Company, Salary,
           (CASE WHEN @prev = Company THEN @rank:= @rank+1 ELSE @rank:=1 END) Rank,
           @prev:= Company patition_key
    FROM Employee
    JOIN (SELECT @rank:=0, @prev:=0) tmp
    ORDER BY Company, Salary) AS Rank_table
WHERE (Company,Rank) in 
    (SELECT * FROM
        ((SELECT Company,(COUNT(ID)+1)/2 AS 'Rank'
         FROM Employee
         GROUP BY Company
         HAVING COUNT(Id)%2=1)
        UNION
        (SELECT Company,COUNT(ID)/2 AS 'Rank'
         FROM Employee
         GROUP BY Company
         HAVING COUNT(Id)%2=0)
        UNION
        (SELECT Company,COUNT(ID)/2+1 AS 'Rank'
         FROM Employee
         GROUP BY Company
         HAVING COUNT(Id)%2=0)) AS A)
ORDER BY Company, Salary
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

# 1194 Echo
"""
SELECT group_id,player_id
FROM
    (SELECT P.group_id, P.player_id, SUM(first_score) AS 'total_score'
    FROM 
        (SELECT first_player, first_score FROM Matches
        UNION ALL
        SELECT second_player,second_score FROM Matches) AS M
    LEFT JOIN Players P
    ON P.player_id = M.first_player
    GROUP BY P.player_id
    ORDER BY group_id, total_score DESC, player_id) final
Group BY group_id
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

# 177
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

# 1132 Echo
"""
SELECT ROUND(100*AVG(Ratio),2) AS 'average_daily_percent'
FROM 
    (SELECT A.action_date, COUNT(R.remove_date)/COUNT(*) AS Ratio
    FROM
    (SElECT DISTINCT post_id,action_date
    FROM Actions 
    WHERE action='report' and extra='spam') AS A
    LEFT JOIN Removals R
    ON A.post_id = R.post_id
    GROUP BY A.action_date) AS B
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

#1098 Echo
"""
SELECT book_id,name 
FROM Books
WHERE available_from < subdate('2019-06-23',interval 1 month)
and book_id not in 
    (SELECT book_id
    FROM Orders
    WHERE dispatch_date between subdate('2019-06-23',interval 1 year) and '2019-06-23'
    GROUP BY book_id
    HAVING SUM(quantity) >= 10)
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
# 550 Echo
"""
SELECT ROUND(
    (SELECT COUNT(DISTINCT A1.player_id) 
    FROM Activity A1
    WHERE (A1.player_id,A1.event_date) 
    in (SELECT A2.player_id, adddate(min(A2.event_date),interval 1 day) 
        FROM Activity A2
        GROUP BY A2.player_id))
    /
    (SELECT COUNT(DISTINCT A3.player_id) FROM Activity A3)
    ,2) AS 'fraction'
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

# 585 Echo
"""
SELECT ROUND(SUM(TIV_2016),2) AS 'TIV_2016'
FROM insurance
WHERE TIV_2015 in (SELECT DISTINCT TIV_2015
                  FROM insurance
                  GROUP BY TIV_2015
                  HAVING COUNT(*)>1)
AND (LAT,LON) in (SELECT DISTINCT LAT,LON
               FROM insurance
               GROUP BY LAT,LON
               HAVING COUNT(*)=1)

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

# 1205 Echo 
# Similar to David's answer
"""
SELECT date_format(TT.trans_date,'%Y-%m') AS 'month',
	country,SUM(state='approved') AS 'approved_count',
	SUM(IF(state='approved',amount,0)) AS 'approved_amount',
	SUM(state='charged') AS 'chargeback_count',
	SUM(IF(state='charged',amount,0)) AS 'chargeback_amount'
FROM
	(SELECT * FROM Transactions
	UNION ALL
	(SELECT trans_id,country,'charged' AS 'state',amount,C.trans_date
 	FROM Chargebacks C
 	LEFT JOIN Transactions T
 	ON C.trans_id = T.id)) AS TT #total
GROUP BY date_format(TT.trans_date,'%Y-%m'),TT.country
HAVING SUM(state='approved')>0 or SUM(state='charged')>0
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

#1174 Echo
"""
SELECT ROUND(100*SUM(D.order_date=D.customer_pref_delivery_date)/COUNT(*),2) 
AS 'immediate_percentage'
FROM Delivery D
WHERE (customer_id,order_date) in 
    (SElECT customer_id,min(order_date)
    FROM Delivery
    GROUP BY customer_id)
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

# 612 Echo
"""
SELECT ROUND(MIN(SQRT(pow(p1.x-p2.x,2)+pow(p1.y-p2.y,2))),2) AS 'shortest'
FROM point_2d p1, point_2d p2
WHERE not (p1.x = p2.x and p1.y = p2.y)
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

# 626 Echo
"""
SELECT S1.id,
IFNULL((CASE
 WHEN S1.id%2=1 THEN (SELECT student FROM seat S2 WHERE S2.id=S1.id+1)
 WHEN S1.id%2=0 THEN (SELECT student FROM seat S3 WHERE S3.id=S1.id-1)
 END),S1.student) AS 'student'
FROM seat S1
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

# 1164 Echo
"""
SELECT P.product_id,IFNULL(A.price,10) AS 'price'
FROM (SELECT DISTINCT product_id FROM Products) AS P
LEFT JOIN 
    (SELECT product_id,new_price AS 'price'
        FROM Products P
        WHERE (product_id,change_date) IN
            (SELECT product_id,MAX(change_date) 
            FROM Products
            WHERE change_date <= '2019-08-16'
            GROUP BY product_id)) AS A
ON P.product_id=A.product_id
"""

# OR
"""
SELECT product_id,new_price AS 'price'
FROM Products P
WHERE (product_id,change_date) IN
    (SELECT product_id,MAX(change_date) 
    FROM Products
    WHERE change_date <= '2019-08-16'
    GROUP BY product_id)
UNION 
SELECT product_id,10 
FROM (SELECT DISTINCT product_id FROM Products) AS A
WHERE product_id not in 
    (SELECT product_id
    FROM Products
    WHERE change_date <= '2019-08-16')
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

# 608 Echo
"""
SELECT DISTINCT id,
(CASE WHEN p_id is null THEN 'Root'
 WHEN p_id is not null and c_id is not null THEN 'Inner'
 ELSE 'Leaf'
 END) AS 'Type'
FROM (
    SELECT t1.id,t1.p_id,t2.p_id AS 'c_id'
    FROM tree t1
    LEFT JOIN tree t2
    ON t1.id = t2.p_id) AS A
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
# 570 Echo
"""
SELECT E2.Name 
FROM Employee E1
JOIN Employee E2
ON E1.ManagerId = E2.Id
GROUP BY E2.Id
HAVING COUNT(*)>=5 
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

# 534 Echo
"""
SELECT A1.player_id, A1.event_date, SUM(A2.games_played) AS 'games_played_so_far'
FROM Activity A1
LEFT JOIN Activity A2
ON A1.player_id = A2.player_id and A1.event_date >= A2.event_date
GROUP BY A1.player_id, A1.event_date
"""

# 1204
"""
SELECT cum_table.person_name
FROM (
    SELECT q.person_name, q.weight, q.turn, (@c_weight:=@c_weight + q.weight) AS "cum_weight"
    FROM Queue q, (SELECT @c_weight:=0) c
    ORDER BY q.turn ) cum_table
WHERE cum_table.cum_weight <= 1000
ORDER BY cum_table.cum_weight DESC
LIMIT 1
"""
# 1204 Echo
"""
SELECT D.person_name
FROM
    (SELECT A.turn, SUM(B.weight) AS cum_weight
    FROM Queue A
    LEFT JOIN Queue B
    ON A.turn >= B.turn
    GROUP BY A.turn) AS C
LEFT JOIN Queue D
ON C.turn = D.turn
WHERE cum_weight <= 1000
ORDER BY cum_weight DESC
LIMIT 1
"""

# 1045
"""
SELECT join_table.customer_id
FROM (
    SELECT c.customer_id, COUNT(DISTINCT p.product_key) AS "num_product"
    FROM Customer c
    JOIN Product p 
    ON c.product_key = p.product_key
    GROUP BY c.customer_id) join_table
WHERE join_table.num_product = (SELECT COUNT(DISTINCT p2.product_key)
                                FROM Product p2)
ORDER BY join_table.customer_id ASC
"""

# 1045 Echo
"""
SELECT customer_id
FROM (SELECT *
      FROM Customer
      WHERE product_key in (SELECT * FROM Product)) AS A
GROUP BY customer_id
HAVING COUNT(DISTINCT product_key) = (SELECT COUNT(product_key) FROM Product)
"""

# 1126
"""
SELECT agg.business_id
FROM (
    SELECT e2.business_id, COUNT(*) AS "count_above_avg"
    FROM Events e2
    LEFT JOIN (
        SELECT e.event_type, AVG(e.occurences) AS "avg_ocur"
        FROM Events e
        GROUP BY e.event_type) sum_table
    ON e2.event_type = sum_table.event_type
    WHERE e2.occurences> sum_table.avg_ocur
    GROUP BY e2.business_id) agg
WHERE agg.count_above_avg > 1
"""

# 1126 Echo
"""
SELECT business_id
FROM
    (SELECT business_id,IF(E.occurences>A.avg_o,1,0) AS 'beat_avg'
    FROM Events E
    LEFT JOIN  
        (SELECT event_type, AVG(occurences) AS 'avg_o'
        FROM Events
        GROUP BY event_type) AS A
    On E.event_type = A.event_type) AS B
GROUP BY business_id
HAVING SUM(beat_avg) > 1 
"""
# OR
"""
SELECT business_id
FROM Events E
LEFT JOIN  
    (SELECT event_type, AVG(occurences) AS 'avg_o'
    FROM Events
    GROUP BY event_type) AS A
On E.event_type = A.event_type
GROUP BY E.business_id
HAVING SUM(IF(E.occurences> A.avg_o,1,0)) >1
"""

# 1077
"""
SELECT p2.project_id, p2.employee_id
FROM Project p2
LEFT JOIN Employee e2
ON p2.employee_id = e2.employee_id
WHERE (p2.project_id, e2.experience_years) IN (
    SELECT p.project_id, MAX(e.experience_years) AS "max_exp"
    FROM Project p
    LEFT JOIN Employee e
    ON p.employee_id = e.employee_id
    GROUP BY p.project_id)
"""

# 176
# use double select to prevent no rows return
"""
SELECT (
    SELECT DISTINCT e.Salary 
    FROM Employee e
    ORDER BY e.Salary DESC 
    LIMIT 1 OFFSET 1 ) AS "SecondHighestSalary"
"""

# 1142
# pay attention to the window case, the length of the windows
"""
SELECT ROUND(IFNULL(AVG(user_table.num_session), 0), 2) AS "average_sessions_per_user"
FROM (
    SELECT a.user_id, COUNT(DISTINCT a.session_id) AS "num_session"
    FROM Activity a
    WHERE a.activity_date BETWEEN DATE_SUB('2019-07-27', INTERVAL 29 DAY)
    AND '2019-07-27'
    GROUP BY a.user_id) user_table
"""

# 196
"""
DELETE p
FROM Person p, Person p2
WHERE p.Email = p2.Email AND p.ID > p2.Id
"""

# 196
# faster
"""
DELETE p
FROM Person p
LEFT JOIN (SELECT MIN(p2.Id) AS 'Id', p2.Email
           FROM Person p2
           GROUP BY p2.Email) group_email
ON p.Id = group_email.Id
WHERE group_email.Email IS NULL
"""
# 196 Echo
"""
DELETE FROM Person WHERE Id NOT IN 
(SELECT * FROM (SELECT MIN(Id) FROM Person GROUP By Email)as A)
"""

# 197
"""
SELECT w.Id
FROM Weather w
LEFT JOIN Weather w2
ON DATE_SUB(w.RecordDate, INTERVAL 1 DAY) = w2.RecordDate
WHERE w.Temperature > w2.Temperature
"""
# 197 Echo
"""
SELECT A.Id
From Weather A Left Join  
Weather B
On subdate(A.RecordDate,1) = B.RecordDate
Where A.Temperature > B.Temperature
"""


# 596
"""
SELECT stu_count.class
FROM (
    SELECT c.class, COUNT(DISTINCT c.student) AS "num_stu"
    FROM courses c
    GROUP BY c.class
    HAVING num_stu >= 5) stu_count
"""

# 596 Echo
"""
SELECT class
FROM courses
GROUP BY class
HAVING count(distinct student) >= 5
"""

# 619
# put operation in HAVING is faster and saving memory
"""
SELECT MAX(count_table.num) AS "num"
FROM (
    SELECT m.num
    FROM my_numbers m
    GROUP BY m.num
    HAVING COUNT(*) = 1) count_table
"""

# 597
# pay attention to the what is the accpet_rate
"""
SELECT ROUND(IFNULL(COUNT(DISTINCT r.requester_id, r.accepter_id)/
       COUNT(DISTINCT f.sender_id, f.send_to_id),0),2) AS "accept_rate"
FROM friend_request f, request_accepted r
"""

# 183
# where cannot be replace by having, since having need to be applied to columns in the select statement
"""
SELECT c.Name AS "Customers"
FROM Customers c
LEFT JOIN Orders o
ON c.Id = o.CustomerId
WHERE o.ID IS NULL
"""

# 1211
"""
SELECT q.query_name, ROUND(AVG(q.rating/q.position),2) AS "quality",
       ROUND(AVG(CASE WHEN q.rating < 3 THEN 1 ELSE 0 END)*100,2) AS "poor_query_percentage"
FROM Queries q
GROUP BY q.query_name
"""

# 1211 Echo
"""
SELECT query_name,ROUND(AVG(rating/position),2) AS quality, 
ROUND(SUM(IF(rating<3,1,0))/COUNT(*)*100,2) AS poor_query_percentage 
FROM Queries
GROUP BY query_name
"""

# 1083
"""
SELECT s.buyer_id
FROM Sales s
LEFT JOIN Product p
ON s.product_id = p.product_id
GROUP BY s.buyer_id
HAVING SUM(CASE WHEN p.product_name = 'S8' THEN 1 ELSE 0 END)>0
AND SUM(CASE WHEN p.product_name = 'iPhone' THEN 1 ELSE 0 END)=0
"""

# 1083
# using in clause is faster
"""
SELECT DISTINCT s2.buyer_id
FROM Sales s2
WHERE s2.buyer_id NOT IN (
    SELECT s.buyer_id
    FROM Sales s
    LEFT JOIN Product p
    ON s.product_id = p.product_id
    WHERE p.product_name = 'iPhone')
AND s2.buyer_id IN (
    SELECT s3.buyer_id
    FROM Sales s3
    LEFT JOIN Product p2
    ON s3.product_id = p2.product_id
    WHERE p2.product_name = 'S8')
"""

# 1083 Echo
"""
SELECT DISTINCT buyer_id
FROM Sales S
LEFT JOIN Product P
On S.product_id = P.product_id
WHERE P.product_name = 'S8'
and buyer_id Not in (SELECT buyer_id FROM Sales S1
                    LEFT JOIN Product P1
                    ON S1.product_id = P1.product_id
                    WHERE P1.product_name='iPhone') 
"""

# 181
"""
SELECT e1.Name AS "Employee"
FROM Employee e1, Employee e2
WHERE e1.ManagerId = e2.Id AND e1.Salary > e2.Salary
"""

# 181
# use join is slightly faster
"""
SELECT e1.Name AS "Employee"
FROM Employee e1
LEFT JOIN Employee e2
ON e1.ManagerId = e2.Id
WHERE e1.Salary > e2.Salary
"""

# 1084
"""
SELECT DISTINCT s.product_id, p.product_name
FROM Sales s
JOIN Product p
ON s.product_id = p.product_id
WHERE s.product_id IN (SELECT s2.product_id
                       FROM Sales s2
                       WHERE s2.sale_date BETWEEN '2019-01-01' AND '2019-03-31') AND s.product_id NOT IN (
                      SELECT s3.product_id
                      FROM Sales s3
                      WHERE s3.sale_date NOT BETWEEN '2019-01-01' AND '2019-03-31')
"""
# 1084 Echo
"""
SELECT Sales.product_id, Product.product_name
FROM Sales
LEFT JOIN Product
ON Sales.product_id = Product.product_id
GROUP BY Sales.product_id
HAVING min(sale_date) >= '2019-01-01' and max(sale_date) <= '2019-03-31'
"""


# 1076
# use having to select rows with max values [return multi-rows]
"""
SELECT p.project_id
FROM Project p
GROUP BY p.project_id
HAVING COUNT(DISTINCT employee_id) = (
    SELECT MAX(count_table.num_count)
    FROM (
        SELECT p2.project_id, COUNT(DISTINCT p2.employee_id) AS "num_count"
        FROM Project p2
        GROUP BY p2.project_id) count_table)
"""

# 1076 Echo
"""
SELECT B.project_id
FROM Project B
GROUP BY B.project_id
HAVING COUNT(B.employee_id) = (SELECT COUNT(employee_id)  as cnt
                            FROM Project  
                            GROUP BY project_id
                            ORDER BY cnt DESC
                            LIMIT 1)
"""

# 1141
"""
SELECT a.activity_date AS "day", COUNT(DISTINCT user_id) AS "active_users"
FROM Activity a
WHERE a.activity_date BETWEEN DATE_SUB('2019-07-27', INTERVAL 29 DAY) AND '2019-07-27'
GROUP BY a.activity_date
"""

# 175
"""
SELECT p.FirstName, p.LastName, a.City, a.State
FROM Person p
LEFT JOIN Address a
ON p.PersonId = a.PersonId
"""

# 512
"""
SELECT a.player_id, a.device_id
FROM Activity a
WHERE (a.player_id, a.event_date) IN (
    SELECT a2.player_id, MIN(a2.event_date)
    FROM Activity a2
    GROUP BY a2.player_id)
"""

# 512 Echo
"""
SELECT A.player_id,A.device_id
FROM Activity A 
INNER JOIN (SELECT player_id,MIN(event_date) as event_date_1 
            FROM Activity Group By player_id) AS B
ON A.player_id = B.player_id and A.event_date = B.event_date_1

"""

# 182
"""
SELECT DISTINCT p1.Email
FROM Person p1, Person p2
WHERE p1.Id < p2.Id AND p1.Email = p2.Email
"""

# 182
# using group by is faster
"""
SELECT p1.Email
FROM Person p1
GROUP BY p1.Email
HAVING COUNT(p1.Id) > 1
"""

# 182 Echo
# using group by and where
"""
Select Email
From (
    Select Email,Count(Email) as cnt
    From Person
    Group By Email) AS A
Where cnt > 1
"""

# 1075
"""
SELECT p.project_id, ROUND(IFNULL(AVG(e.experience_years),0),2) AS "average_years"
FROM Project p
LEFT JOIN Employee e
ON p.employee_id = e.employee_id
GROUP BY p.project_id
"""

# 607
"""
SELECT s2.name
FROM salesperson s2
WHERE s2.sales_id NOT IN (
    SELECT s.sales_id
    FROM salesperson s
    LEFT JOIN orders o
    ON s.sales_id = o.sales_id
    JOIN company c
    ON o.com_id = c.com_id
    WHERE c.name = "RED")
"""

# 1113
"""
SELECT a.extra AS "report_reason", COUNT(DISTINCT a.post_id) AS "report_count"
FROM Actions a
WHERE a.action_date = DATE_SUB('2019-07-05', INTERVAL 1 DAY) AND a.action = 'report'
GROUP BY a.extra
"""

# 603
"""
SELECT c.seat_id
FROM cinema c
LEFT JOIN cinema c2
ON c.seat_id + 1 = c2.seat_id 
LEFT JOIN cinema c3
ON c.seat_id - 1 = c3.seat_id 
WHERE (c.free = 1 AND c2.free = 1) OR (c.free = 1 AND c3.free = 1)
"""

# 603 Echo
"""
SELECT DISTINCT A.seat_id
FROM cinema A, cinema B
WHERE (A.seat_id +1 = B.seat_id and A.free * B.free =1) 
or (A.seat_id -1 = B.seat_id and A.free * B.free =1 )
"""

# 577
"""
SELECT e.name, b.bonus
FROM Employee e
LEFT JOIN Bonus b
ON e.empId = b.empId
WHERE IFNULL(b.bonus,0) < 1000
"""

# 610
"""
SELECT t.x, t.y, t.z,  
       CASE WHEN (t.x + t.y > t.z) AND (t.x + t.z > t.y) AND (t.y + t.z > t.x) THEN "Yes" ELSE "No" END AS "triangle"
FROM triangle t
"""

# 610 Echo, answer from https://leetcode.com/gdianov/ 
"""
select *, 
    IF(x + y > z AND x + z > y AND y + z > x, 'Yes', 'No') as triangle 
    from triangle;
"""

# 620
"""
SELECT c.id, c.movie, c.description, c.rating
FROM cinema c
WHERE MOD(c.id,2) = 1 AND c.description != "boring"
ORDER BY c.rating DESC
"""

# 1179
# SUM operation will ignore NULL
"""
SELECT d.id,
       SUM(CASE WHEN d.month = 'Jan' THEN d.revenue ELSE NULL END) AS "Jan_Revenue",
       SUM(CASE WHEN d.month = 'Feb' THEN d.revenue ELSE NULL END) AS "Feb_Revenue",
       SUM(CASE WHEN d.month = 'Mar' THEN d.revenue ELSE NULL END) AS "Mar_Revenue",
       SUM(CASE WHEN d.month = 'Apr' THEN d.revenue ELSE NULL END) AS "Apr_Revenue",
       SUM(CASE WHEN d.month = 'May' THEN d.revenue ELSE NULL END) AS "May_Revenue",
       SUM(CASE WHEN d.month = 'Jun' THEN d.revenue ELSE NULL END) AS "Jun_Revenue",
       SUM(CASE WHEN d.month = 'Jul' THEN d.revenue ELSE NULL END) AS "Jul_Revenue",
       SUM(CASE WHEN d.month = 'Aug' THEN d.revenue ELSE NULL END) AS "Aug_Revenue",
       SUM(CASE WHEN d.month = 'Sep' THEN d.revenue ELSE NULL END) AS "Sep_Revenue",
       SUM(CASE WHEN d.month = 'Oct' THEN d.revenue ELSE NULL END) AS "Oct_Revenue",
       SUM(CASE WHEN d.month = 'Nov' THEN d.revenue ELSE NULL END) AS "Nov_Revenue",
       SUM(CASE WHEN d.month = 'Dec' THEN d.revenue ELSE NULL END) AS "Dec_Revenue"
FROM Department d
GROUP BY d.id
"""

# 586
"""
SELECT o.customer_number
FROM orders o
GROUP BY o.customer_number
HAVING COUNT(*) = (SELECT COUNT(*) AS "count_num"
                   FROM orders o2
                   GROUP BY o2.customer_number
                   ORDER BY count_num DESC
                   LIMIT 1)
"""

# 586 Echo
"""
SELECT customer_number 
FROM   (SELECT customer_number, 
               Count(order_number) AS cnt 
        FROM   orders 
        GROUP  BY customer_number) AS A 
ORDER  BY cnt DESC 
LIMIT  1 
"""

# 584
#  WHEN SET c.referee_id,0 != 2, NULL will be ignore, since SQL thinks that the value is empty
"""
SELECT c.name
FROM customer c
WHERE IFNULL(c.referee_id,0) != 2
"""

# 1148
"""
SELECT DISTINCT v.author_id AS "id"
FROM Views v
WHERE v.author_id = v.viewer_id
ORDER BY v.author_id
"""

#1082
"""
SELECT s.seller_id
FROM Sales s
GROUP BY s.seller_id
HAVING SUM(s.price) = (
    SELECT SUM(s2.price) AS "sum_price"
    FROM Sales s2
    GROUP BY s2.seller_id
    ORDER BY sum_price DESC
    LIMIT 1)
"""

# 627
"""
UPDATE salary
SET sex = CASE WHEN salary.sex = 'm' THEN 'f'
               ELSE 'm' END
"""

# 627 Echo
"""
UPDATE salary
SET SEX = IF(sex='m','f','m')
"""

# 1050
"""
SELECT a.actor_id, a.director_id
FROM ActorDirector a
GROUP BY a.actor_id, a.director_id
HAVING COUNT(*) >= 3
"""

# 1173
"""
SELECT ROUND(COUNT(DISTINCT CASE WHEN d.order_date = d.customer_pref_delivery_date THEN d.delivery_id END)/COUNT(DISTINCT d.delivery_id)*100,2) AS "immediate_percentage"
FROM Delivery d
"""

# 613
"""
SELECT MIN(p2.x - p.x) AS "shortest"
FROM point p, point p2
WHERE p.x < p2.x
"""

# 613
# slightly faster
"""
SELECT MIN(p2.x - p.x) AS "shortest"
FROM point p
LEFT JOIN point p2
ON p.x < p2.x
"""

# 613 Echo
"""
SELECT min(distance) AS 'shortest'
FROM point A
LEFT JOIN (SELECT B.x, MIN(ABS( B.x-C.x )) as distance
           FROM point B, point C
           WHERE B.x <> C.x) AS D
ON A.x = D.x

*/ Method 2
SELECT min(abs(A.x-B.x)) AS 'shortest'
FROM point A, point B
WHERE A.x <> B.x   
*/

"""

# 595
"""
SELECT w.name, w.population, w.area
FROM World w
WHERE w.area > 3000000 OR w.population > 25000000
"""

# 511
"""
SELECT a.player_id, MIN(a.event_date) AS "first_login"
FROM Activity a
GROUP BY a.player_id
"""

# 1069
"""
SELECT s.product_id, SUM(s.quantity) AS "total_quantity"
FROM Sales s
GROUP BY s.product_id
"""

# 1068
"""
SELECT p.product_name, s.year, s.price
FROM Sales s
JOIN Product p
ON s.product_id = p.product_id
"""

# 1068
# faster by using distinct for joining
"""
SELECT p.product_name, s.year, s.price
FROM Product p
JOIN (SELECT DISTINCT *
      FROM Sales) s
ON p.product_id = s.product_id
"""

# 1225
# we first union Failed and Succeeded table together, then filter the specific date. 
# Then we use @ function to find out the date when status changes, split the data into different status groups and groupby each status group period.
"""
SELECT grouped_table.status AS "period_state",
       MIN(grouped_table.date) AS "start_date",
       MAX(grouped_table.next_date) AS "end_date"
FROM ( 
    SELECT final_table.*, (@rm:=@rm + CASE WHEN @nr=@nr:=final_table.next_status THEN 0
                                     ELSE 1 END) AS "chg_ind"
    FROM (
        SELECT clean1.*,
               IFNULL(clean2.date,clean1.date) AS 'next_date', 
               IFNULL(clean2.status, clean1.status) AS "next_status"
        FROM (SELECT @rm:=0) temp,
           (SELECT @nr:= (SELECT t2.status
                            FROM (SELECT f.fail_date AS 'date', 'failed' AS "status"
                                  FROM Failed f
                                  UNION (SELECT s.success_date, 'succeeded' AS "status"
                                         FROM Succeeded s)
                                  ORDER BY date
                                  LIMIT 1) t2)) t,
            (
            SELECT p1.*
            FROM (     
                SELECT f.fail_date AS 'date', 'failed' AS "status"
                FROM Failed f
                UNION (SELECT s.success_date, 'succeeded' AS "status"
                       FROM Succeeded s)
                ORDER BY date) p1
            WHERE p1.date BETWEEN '2019-01-01' AND '2019-12-31' )clean1
        LEFT JOIN (
            SELECT p2.*
            FROM (
                SELECT f.fail_date AS 'date', 'failed' AS "status"
                FROM Failed f
                UNION (SELECT s.success_date, 'succeeded' AS "status"
                       FROM Succeeded s)
                ORDER BY date) p2
            WHERE p2.date BETWEEN '2019-01-01' AND '2019-12-31') clean2
        ON DATE_ADD(clean1.date, INTERVAL 1 DAY) = clean2.date AND clean1.status = clean2.status 
        ) final_table
    ) grouped_table
GROUP BY grouped_table.chg_ind
"""

# 1225 Echo
"""
(SELECT 'succeeded' AS 'period_state', Min(success_date) AS 'start_date',
        Max(success_date) AS 'end_date'
FROM
    (SELECT S1.success_date, (@row_number1:=@row_number1+1) AS 'row1'
    FROM Succeeded S1, (SELECT @row_number1:=0) a
    WHERE success_date between '2019-01-01' and '2019-12-31') AS S2
GROUP BY SUBDATE(success_date,interval row1 day))
UNION
(SELECT 'failed' AS 'period_state', Min(fail_date) AS 'fail_date',
        Max(fail_date) AS 'end_date'
FROM
    (SELECT F1.fail_date, (@row_number2:=@row_number2+1) AS 'row2'
    FROM Failed F1,(SELECT @row_number2:=0) a
    WHERE fail_date between '2019-01-01' and '2019-12-31') AS F2
GROUP BY SUBDATE(fail_date,interval row2 day))
ORDER BY start_date
"""

# 1241
"""
SELECT DISTINCT s.sub_id AS "post_id", IFNULL(count_table.number_of_comments,0) AS "number_of_comments"
FROM Submissions s
LEFT JOIN (
    SELECT s2.parent_id, COUNT(DISTINCT s2.sub_id) AS "number_of_comments"
    FROM Submissions s2
    WHERE s2.parent_id IS NOT NULL
    GROUP BY s2.parent_id ) count_table
ON s.sub_id = count_table.parent_id
WHERE s.parent_id IS NULL
ORDER BY s.sub_id
"""

# 1251
"""
SELECT p.product_id, ROUND(SUM(p.price * u.units)/SUM(u.units),2) AS 'average_price'
FROM UnitsSold u
LEFT JOIN Prices p
ON u.product_id = p.product_id
AND u.purchase_date between p.start_date and p.end_date
GROUP BY p.product_id
"""

# 1264
"""
SELECT DISTINCT l.page_id AS 'recommended_page'
FROM Friendship f
JOIN Likes l
ON CASE WHEN f.user1_id = 1 THEN f.user2_id
        WHEN f.user2_id = 1 THEN f.user1_id
   END = l.user_id
AND l.page_id NOT IN (SELECT l2.page_id FROM Likes l2 WHERE l2.user_id = 1)
"""

# 1270
"""
SELECT e3.Employee_id
FROM Employees e1
LEFT JOIN Employees e2
ON e1.Employee_id = e2.manager_id
LEFT JOIN Employees e3
ON e2.Employee_id = e3.manager_id
WHERE e1.manager_id = 1
AND e3.Employee_id != 1
"""

# 1280
"""
SELECT s.student_id, s.student_name, sj.subject_name, IFNULL(counts.exam_count, 0) AS 'attended_exams'
FROM Students s
LEFT JOIN Subjects sj
ON 1=1
LEFT JOIN (
    SELECT e.student_id, e.subject_name, count(1) AS 'exam_count'
    FROM Examinations e
    GROUP BY e.student_id, e.subject_name
    ) counts
ON s.student_id = counts.student_id
AND sj.subject_name = counts.subject_name
WHERE sj.subject_name IS NOT NULL
ORDER BY s.student_id ASC, sj.subject_name ASC
"""

# 1285
"""
SELECT MIN(g.log_id) AS 'start_id', MAX(g.log_id) AS 'end_id'
FROM (
    SELECT l.log_id, (l.log_id - ROW_NUMBER() OVER()) AS group_id
    FROM Logs l
    ) g
GROUP BY g.group_id
ORDER BY start_id ASC
"""

# 1294
"""
SELECT avg_table.country_name
      ,CASE WHEN avg_table.avg_temp <= 15 THEN 'Cold'
            WHEN avg_table.avg_temp >= 25 THEN 'Hot'
            ELSE 'Warm'
       END AS 'weather_type'
FROM (
    SELECT c.country_name
           ,AVG(w.weather_state) AS 'avg_temp'
    FROM Countries c
    LEFT JOIN Weather w
    ON c.country_id = w.country_id
    WHERE MONTH(w.day) = 11
    AND YEAR(w.day) = 2019
    GROUP BY c.country_name
    ) avg_table
"""

# 1303
"""
SELECT e2.employee_id, size.team_size
FROM Employee e2
LEFT JOIN (
    SELECT e.team_id, count(1) AS 'team_size'
    FROM Employee e
    GROUP BY e.team_id
    ) size
ON e2.team_id = size.team_id
"""

# 1308
"""
SELECT s.gender, s.day, SUM(s.score_points) OVER(PARTITION BY s.gender ORDER BY s.day ASC) AS 'total'
FROM Scores s
"""

# 1321
"""
SELECT c.visited_on, SUM(c2.amount) AS 'amount', ROUND(SUM(c2.amount)/7, 2) AS 'average_amount'
FROM (SELECT Customer.visited_on, SUM(Customer.amount) AS 'amount'
      FROM Customer
      GROUP BY Customer.visited_on
      ) c
INNER JOIN Customer c2
ON c.visited_on <= DATE_ADD(c2.visited_on, INTERVAL 6 DAY)
AND c.visited_on >= c2.visited_on
AND c.visited_on >= DATE_ADD((SELECT MIN(Customer.visited_on) FROM Customer), INTERVAL 6 DAY)
GROUP BY c.visited_on
"""

# 1322
"""
SELECT a.ad_id, ROUND(CASE WHEN SUM(CASE WHEN a.action in ('Clicked', 'Viewed') THEN 1 ELSE 0 END) = 0 THEN 0
                     ELSE SUM(CASE WHEN a.action = 'Clicked' THEN 1 ELSE 0 END)/ SUM(CASE WHEN a.action in ('Clicked', 'Viewed') THEN 1 ELSE 0 END)
                     END * 100, 2) AS 'ctr'
FROM Ads a
GROUP BY a.ad_id
ORDER BY ctr DESC, a.ad_id ASC
"""

# 1327
"""
SELECT p.product_name, SUM(o.unit) AS 'unit'
FROM Products p
LEFT JOIN Orders o
ON p.product_id = o.product_id
WHERE MONTH(o.order_date) = 2 AND YEAR(o.order_date) = 2020
GROUP BY p.product_name
HAVING unit >= 100
"""

# 1336
"""
WITH visits_table AS (

    SELECT g.transaction_count, COUNT(g.user_id) AS 'visits_count'
    FROM (
        SELECT v.user_id, v.visit_date, SUM(CASE WHEN t.amount IS NULL THEN 0
                                            ELSE 1 END) AS 'transaction_count'
        FROM Visits v
        LEFT JOIN Transactions t
        ON v.user_id = t.user_id
        AND v.visit_date = t.transaction_date
        GROUP BY v.user_id, v.visit_date
        ) g
    GROUP BY g.transaction_count
    ORDER BY g.transaction_count ASC 
    ),

cte_count AS (
    WITH RECURSIVE rec_cte_count AS (
        SELECT 0 AS counts
        UNION ALL 
        SELECT counts + 1 AS counts
        FROM rec_cte_count
        WHERE counts <= (SELECT MAX(transaction_count) FROM visits_table)
        )
    SELECT counts FROM rec_cte_count
    )


select * from cte_count
"""

# 1341
"""SELECT result1.name AS 'results'
FROM (
    SELECT u.name, COUNT(1) AS 'user_counts'
    FROM Movie_Rating m
    LEFT JOIN Users u
    ON m.user_id = u.user_id
    GROUP BY u.name
    ORDER BY user_counts DESC, u.name ASC
    LIMIT 1
    ) result1

UNION ALL

SELECT result2.title AS 'results'
FROM (
    SELECT m3.title, AVG(m2.rating) AS 'movie_rates'
    FROM Movie_Rating m2
    LEFT JOIN Movies m3
    ON m2.movie_id = m3.movie_id
    WHERE MONTH(m2.created_at) = 2 AND YEAR(m2.created_at) = 2020
    GROUP BY m3.title
    ORDER BY movie_rates DESC, m3.title ASC
    LIMIT 1
    ) result2

"""

# 1350
"""
SELECT s.id, s.name 
FROM Students s
LEFT JOIN Departments d on s.department_id = d.id
WHERE d.name is null
"""

# 1355
"""
WITH activity_count AS (
    SELECT f.activity, COUNT(1) AS 'act_counts'
    FROM Friends f
    GROUP BY f.activity
)


SELECT a.activity
FROM activity_count a
WHERE a.act_counts != (SELECT MAX(act_counts) FROM activity_count)
AND a.act_counts != (SELECT MIN(act_counts) FROM activity_count)
"""

# 1364
"""
SELECT i.invoice_id
      ,c2.customer_name
      ,i.price
      ,SUM(CASE WHEN c3.contact_email IS NULL THEN 0
           ELSE 1 END) AS 'contacts_cnt'
      ,SUM(CASE WHEN c4.email IS NULL THEN 0
           ELSE 1 END) AS 'trusted_contacts_cnt'
      
      
FROM Invoices i

-- get client name
LEFT JOIN Customers c2
ON c2.customer_id = i.user_id


-- get contacts
LEFT JOIN Contacts c3
ON i.user_id = c3.user_id
LEFT JOIN Customers c4
ON c4.email = c3.contact_email

GROUP BY i.invoice_id, c2.customer_name, i.price
ORDER BY i.invoice_id ASC
"""

# 1369
"""
WITH order_table AS (
    SELECT u.username, u.activity, u.startDate, u.endDate
    ,ROW_NUMBER() OVER(PARTITION BY u.username ORDER BY u.startDate DESC) AS 'order'
    ,COUNT(1) OVER(PARTITION BY u.username) AS 'act_count'
    FROM UserActivity u
    )

SELECT o.username, o.activity, o.startDate, o.endDate
FROM order_table o
WHERE o.order = 2 OR o.act_count = 1
"""

# 1378
"""
SELECT ei.unique_id, e.name
FROM Employees e
LEFT JOIN EmployeeUNI ei
ON e.id = ei.id
"""

# 1384
"""
WITH table2018 AS (
    SELECT s.product_id
          ,p.product_name
          ,'2018' AS 'report_year'
          ,(DATEDIFF(LEAST(s.period_end, '2018-12-31') , GREATEST(s.period_start, '2018-01-01')) + 1) * s.average_daily_sales AS 'total_amount'
    FROM Sales s
    LEFT JOIN Product p
    ON s.product_id = p.product_id
    WHERE YEAR(s.period_start) <= 2018 AND YEAR(s.period_end) >= 2018
    ),
    
    table2019 AS (
    SELECT s.product_id
          ,p.product_name
          ,'2019' AS 'report_year'
          ,(DATEDIFF(LEAST(s.period_end, '2019-12-31') , GREATEST(s.period_start, '2019-01-01')) + 1) * s.average_daily_sales AS 'total_amount'
    FROM Sales s
    LEFT JOIN Product p
    ON s.product_id = p.product_id
    WHERE YEAR(s.period_start) <= 2019 AND YEAR(s.period_end) >= 2019
    ),
    
    table2020 AS (
    SELECT s.product_id
          ,p.product_name
          ,'2020' AS 'report_year'
          ,(DATEDIFF(LEAST(s.period_end, '2020-12-31') , GREATEST(s.period_start, '2020-01-01')) + 1) * s.average_daily_sales AS 'total_amount'
    FROM Sales s
    LEFT JOIN Product p
    ON s.product_id = p.product_id
    WHERE YEAR(s.period_start) <= 2020 AND YEAR(s.period_end) >= 2020
    )


SELECT * 
FROM table2018 
UNION ALL (SELECT * FROM table2019)
UNION ALL (SELECT * FROM table2020)
ORDER BY product_id ASC, report_year ASC
"""

# 1393
"""
SELECT s.stock_name
      ,SUM(CASE WHEN s.operation = 'Buy' THEN -1 * s.price
           ELSE s.price END) AS 'capital_gain_loss'
FROM Stocks s
GROUP BY s.stock_name
"""

# 1398
"""
SELECT final.customer_id, final.customer_name
FROM (
    SELECT o.customer_id, c.customer_name
          ,SUM(CASE WHEN o.product_name = 'A' THEN 1 ELSE 0 END) AS 'a_counts'
          ,SUM(CASE WHEN o.product_name = 'B' THEN 1 ELSE 0 END) AS 'b_counts'
          ,SUM(CASE WHEN o.product_name = 'C' THEN 1 ELSE 0 END) AS 'c_counts'
    FROM Orders o
    LEFT JOIN Customers c
    ON o.customer_id = c.customer_id
    GROUP BY o.customer_id, c.customer_name
    ) final
WHERE final.a_counts = 1 AND final.b_counts = 1 AND final.c_counts = 0
"""

# 1407
"""
SELECT u.name, IFNULL(SUM(r.distance), 0) AS 'travelled_distance'
FROM Users u
LEFT JOIN Rides r
ON r.user_id = u.id
GROUP BY u.name
ORDER BY travelled_distance DESC, u.name ASC
"""

# 1412
"""
WITH min_max AS (
    SELECT e.exam_id
          ,MIN(e.score) AS 'min_score'
          ,MAX(e.score) AS 'max_score'
    FROM Exam e
    GROUP BY e.exam_id
    ),
    
    not_quite AS (
        SELECT mm.exam_id, e2.student_id
        FROM min_max mm
        LEFT JOIN Exam e2
        ON mm.exam_id = e2.exam_id
        WHERE e2.score = mm.min_score OR e2.score = mm.max_score
    )
    
SELECT *
FROM Student s
WHERE s.student_id IN (SELECT student_id FROM Exam)
AND s.student_id NOT IN (SELECT student_id FROM not_quite)
"""

# 1421
"""
SELECT q.id, q.year, IFNULL(n.NPV, 0) AS 'npv'
FROM Queries q
LEFT JOIN NPV n
ON q.id = n.id AND q.year = n.year
"""

# 1435
"""
WITH bins AS (
    SELECT "[0-5>" AS bin
    UNION ALL SELECT "[5-10>" AS bin
    UNION ALL SELECT "[10-15>" AS bin
    UNION ALL SELECT "15 or more" AS bin
)

SELECT bins.bin, IFNULL(bin_result.total, 0) AS 'total'
FROM bins
LEFT JOIN (
    SELECT b.bin, COUNT(1) AS "total"
    FROM (
        SELECT CASE WHEN s.duration < 5 * 60 THEN "[0-5>"
                    WHEN s.duration < 10 * 60 THEN "[5-10>"
                    WHEN s.duration < 15 * 60 THEN "[10-15>"
                    ELSE "15 or more" END AS 'bin'
        FROM Sessions s
        ) b
    GROUP BY b.bin
    ) bin_result
ON bins.bin = bin_result.bin
"""

# 1440
"""
SELECT e.left_operand
      ,e.operator
      ,e.right_operand
      ,CASE WHEN e.operator = '>' THEN (CASE WHEN v1.value > v2.value THEN 'true' ELSE 'false' END)
           WHEN e.operator = '=' THEN (CASE WHEN v1.value = v2.value THEN 'true' ELSE 'false' END)
           ELSE (CASE WHEN v1.value < v2.value THEN 'true' ELSE 'false' END)
      END AS 'value'

      
FROM Expressions e
LEFT JOIN `Variables` v1
ON e.left_operand = v1.name
LEFT JOIN `Variables` v2
ON e.right_operand = v2.name
"""

# 1445
"""
WITH apple_table AS (
    SELECT s.sale_date, s.sold_num
    FROM Sales s
    WHERE s.fruit = 'apples'
), orange_table AS (
    SELECT s2.sale_date, s2.sold_num
    FROM Sales s2
    WHERE s2.fruit = 'oranges'
)


SELECT IFNULL(a.sale_date, o.sale_date) AS 'sale_date'
      ,IFNULL(a.sold_num, 0) - IFNULL(o.sold_num, 0) AS 'diff'
FROM apple_table a
JOIN orange_table o
ON a.sale_date = o.sale_date
ORDER BY sale_date ASC
"""

# 1454
"""
SELECT DISTINCT count_table.id, a.name
FROM (
    SELECT l.id, COUNT(DISTINCT l2.login_date) AS 'counts'
    FROM Logins l
    LEFT JOIN Logins l2
    ON DATEDIFF(l.login_date, l2.login_date) < 5
    AND l.login_date >= l2.login_date
    AND l.id = l2.id
    GROUP BY l.id, l.login_date
    ) count_table
LEFT JOIN Accounts a
ON a.id = count_table.id
WHERE count_table.counts >= 5
"""

# 1459
"""
SELECT p.id AS 'p1', p1.id AS 'p2', ABS(p1.x_value - p.x_value) * ABS(p1.y_value - p.y_value) AS 'area'
FROM Points p
LEFT JOIN Points p1
ON p.x_value != p1.x_value
AND p.y_value != p1.y_value
AND p.id < p1.id
HAVING area > 0
ORDER BY area DESC, p1 ASC, p2 ASC
"""

# 1468
"""
WITH tax_table AS (
    SELECT s.company_id, MAX(s.salary) AS 'max_salary'
    FROM Salaries s
    GROUP BY s.company_id
)

SELECT s2.company_id, s2.employee_id, s2.employee_name
      ,ROUND((1 - CASE WHEN t.max_salary < 1000 THEN 0
            WHEN t.max_salary <= 10000 THEN 24/100
            WHEN t.max_salary > 10000 THEN 49/100
       END) * s2.salary, 0) AS 'salary' 
FROM Salaries s2
LEFT JOIN tax_table t
ON s2.company_id = t.company_id
"""

# 1479
"""
SELECT i.item_category AS 'CATEGORY'
      ,SUM(CASE WHEN DAYOFWEEK(o.order_date) = 2 THEN IFNULL(o.quantity, 0) ELSE 0 END) AS 'MONDAY'
      ,SUM(CASE WHEN DAYOFWEEK(o.order_date) = 3 THEN IFNULL(o.quantity, 0) ELSE 0 END) AS 'TUESDAY'
      ,SUM(CASE WHEN DAYOFWEEK(o.order_date) = 4 THEN IFNULL(o.quantity, 0) ELSE 0 END) AS 'WEDNESDAY'
      ,SUM(CASE WHEN DAYOFWEEK(o.order_date) = 5 THEN IFNULL(o.quantity, 0) ELSE 0 END) AS 'THURSDAY'
      ,SUM(CASE WHEN DAYOFWEEK(o.order_date) = 6 THEN IFNULL(o.quantity, 0) ELSE 0 END) AS 'FRIDAY'
      ,SUM(CASE WHEN DAYOFWEEK(o.order_date) = 7 THEN IFNULL(o.quantity, 0) ELSE 0 END) AS 'SATURDAY'
      ,SUM(CASE WHEN DAYOFWEEK(o.order_date) = 1 THEN IFNULL(o.quantity, 0) ELSE 0 END) AS 'SUNDAY'
FROM Orders o
RIGHT JOIN Items i
ON o.item_id = i.item_id
GROUP BY i.item_category
ORDER BY i.item_category ASC
"""

# 1484
"""
SELECT a.sell_date, COUNT(DISTINCT a.product) AS 'num_sold'
      ,GROUP_CONCAT(DISTINCT a.product ORDER BY a.product ASC SEPARATOR ',') AS 'products'
FROM Activities a
GROUP BY a.sell_date
"""

# 1495
"""
SELECT DISTINCT c.title
FROM TVProgram t
LEFT JOIN Content c
ON t.content_id = c.content_id
WHERE MONTH(t.program_date) = 6
AND YEAR(t.program_date) = 2020
AND c.Kids_content = 'Y'
AND c.content_type = 'Movies'
"""

# 1501
"""
WITH id2country AS (
    SELECT p.id, p.name, c.name AS 'country_name'
    FROM Person p
    LEFT JOIN Country c
    ON SUBSTRING(p.phone_number, 1, 3) = c.country_code
), caller_flatten AS (
    SELECT c1.caller_id AS 'id', c1.duration
    FROM Calls c1
    UNION ALL
    SELECT c2.callee_id AS 'id', c2.duration
    FROM Calls c2
), duration AS (
    SELECT i.country_name, AVG(c3.duration) AS 'avg_duration'
    FROM caller_flatten c3
    LEFT JOIN id2country i
    ON c3.id = i.id
    GROUP BY i.country_name
)

SELECT d.country_name AS 'country'
FROM duration d
WHERE d.avg_duration > (SELECT AVG(duration)
                        FROM Calls)
"""

# 1511
"""
SELECT s.customer_id, c.name
FROM (
    SELECT o.customer_id
          ,SUM(CASE WHEN MONTH(o.order_date) = 6 AND YEAR(o.order_date) = 2020 THEN p.price * o.quantity 
                    ELSE 0 END) AS "June"
          ,SUM(CASE WHEN MONTH(o.order_date) = 7 AND YEAR(o.order_date) = 2020 THEN p.price * o.quantity 
                    ELSE 0 END) AS "July"
    FROM Orders o
    LEFT JOIN Product p
    ON o.product_id = p.product_id
    GROUP BY o.customer_id
    ) s
LEFT JOIN Customers c
ON c.customer_id = s.customer_id
WHERE s.June >= 100 AND s.July >= 100
"""

# 1517
"""
SELECT *
FROM Users u
WHERE u.mail REGEXP '^[A-Za-z]+[A-Za-z0-9_.-]*@leetcode.com'
"""

# 1527
"""
SELECT *
FROM Patients p
WHERE p.conditions LIKE '% DIAB1%' 
OR p.conditions LIKE 'DIAB1%'
"""

# 1532
"""
SELECT c.name AS 'customer_name'
      ,r.customer_id
      ,r.order_id
      ,r.order_date
FROM (
    SELECT o.order_id
          ,o.order_date
          ,o.customer_id
          ,ROW_NUMBER() OVER(PARTITION BY o.customer_id ORDER BY o.order_date DESC) AS 'row_number'
    FROM Orders o
    ) r
LEFT JOIN Customers c
ON c.customer_id = r.customer_id
WHERE r.row_number <= 3
ORDER BY customer_name ASC, customer_id ASC, order_date DESC
"""

# 1543
"""
SELECT TRIM(LOWER(s.product_name)) AS 'product_name', DATE_FORMAT(s.sale_date, '%Y-%m') AS 'sale_date', COUNT(1) AS 'total'
FROM Sales s
GROUP BY TRIM(LOWER(s.product_name)) , DATE_FORMAT(s.sale_date, '%Y-%M')
ORDER BY product_name ASC, sale_date ASC
"""

# 1549
"""
SELECT p.product_name
      ,r.product_id
      ,o2.order_id
      ,o2.order_date
FROM (
    SELECT o.product_id, MAX(o.order_date) AS 'max_date'
    FROM Orders o
    GROUP BY o.product_id
    ) r
JOIN Orders o2
ON o2.product_id = r.product_id
AND o2.order_date = r.max_date

LEFT JOIN Products p
ON r.product_id = p.product_id
ORDER BY product_name ASC, product_id ASC, order_id ASC
"""

# 1555
"""
SELECT u2.user_id, u2.user_name, u2.credit + IFNULL(r.total_amount, 0) AS 'credit'
      ,CASE WHEN u2.credit + IFNULL(r.total_amount, 0) < 0 THEN 'Yes'
            ELSE 'No' END AS 'credit_limit_breached'
FROM Users u2
LEFT JOIN (
    SELECT u.user_id
          ,SUM(CASE WHEN t1.paid_by = u.user_id THEN -1 * t1.amount
                    ELSE t1.amount END) AS 'total_amount'
    FROM Users u
    LEFT JOIN Transactions t1
    ON t1.paid_by = u.user_id
    OR t1.paid_to = u.user_id
    GROUP BY u.user_id
    ) r
ON u2.user_id = r.user_id
"""

# 1565
"""
SELECT DATE_FORMAT(o.order_date, '%Y-%m') AS 'month'
      ,COUNT(DISTINCT o.order_id) AS 'order_count'
      ,COUNT(DISTINCT o.customer_id) AS 'customer_count'
FROM Orders o
WHERE o.invoice > 20
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
"""

# 1571
"""
SELECT w.name AS 'warehouse_name', SUM(w.units * p.Width * p.Length * p.Height) AS 'volume'
FROM Warehouse w
LEFT JOIN Products p
ON w.product_id = p.product_id
GROUP BY w.name
"""

# 1581
"""
SELECT v.customer_id, COUNT(1) AS 'count_no_trans'
FROM Visits v
LEFT JOIN Transactions t
ON v.visit_id = t.visit_id
WHERE t.visit_id IS NULL
GROUP BY v.customer_id
"""

# 1587
"""
SELECT u.name, SUM(t.amount) AS 'balance'
FROM Users u
LEFT JOIN Transactions t
ON u.account = t.account
GROUP BY t.account
HAVING balance > 10000
"""

# 1596
"""
WITH orders_group AS (
    SELECT o.customer_id, o.product_id, COUNT(1) AS 'product_count'
    FROM Orders o
    GROUP BY o.customer_id, o.product_id
), most_order AS (
    SELECT og.customer_id, MAX(og.product_count) AS 'max_product'
    FROM orders_group og
    GROUP BY og.customer_id
)

SELECT o1.customer_id, o1.product_id, p.product_name
FROM orders_group o1
JOIN most_order m
ON o1.customer_id = m.customer_id
AND o1.product_count = m.max_product
LEFT JOIN Products p
ON o1.product_id = p.product_id
"""

# 1607
"""
SELECT s2.seller_name
FROM Seller s2
WHERE s2.seller_name NOT IN (
    SELECT s.seller_name
    FROM Orders o
    LEFT JOIN Seller s
    ON o.seller_id = s.seller_id
    WHERE YEAR(sale_date) = 2020
)
ORDER BY s2.seller_name ASC
"""

# 1613
"""
WITH RECURSIVE id_table AS (
    SELECT 1 AS customer_id
    UNION ALL
    SELECT customer_id + 1
    FROM id_table
    WHERE customer_id + 1 <= (SELECT MAX(customer_id) FROM Customers)
)

SELECT i.customer_id AS 'ids'
FROM id_table i
WHERE i.customer_id NOT IN (SELECT customer_id FROM Customers)
ORDER BY customer_id ASC
"""

# 1626
"""
SELECT a.student_name AS 'member_A'
      ,b.student_name AS 'member_B'
      ,c.student_name AS 'member_C'
FROM SchoolA a
JOIN SchoolB b
ON a.student_id <> b.student_id
AND a.student_name <> b.student_name
JOIN SchoolC c
ON a.student_id <> c.student_id
AND a.student_name <> c.student_name
AND b.student_id <> c.student_id
AND b.student_name <> c.student_name
"""

# 1633
"""
SELECT r.contest_id, ROUND(COUNT(1) * 100 / (SELECT COUNT(user_id) FROM Users), 2) AS 'percentage'
FROM Register r
GROUP BY r.contest_id
ORDER BY percentage DESC, contest_id ASC
"""

# 1635
"""
WITH RECURSIVE months AS (
    SELECT 1 AS 'month',
           2020 AS 'year'
    UNION ALL
    SELECT month + 1, year
    FROM months
    WHERE month < 12
), active_drivers AS (
    SELECT m.month, COUNT(d.driver_id) AS 'active_drivers'
    FROM months m
    LEFT JOIN Drivers d
    ON m.year > YEAR(d.join_date)
    OR (m.month >= MONTH(d.join_date) AND m.year = YEAR(d.join_date))
    GROUP BY m.month
), accepted_rides AS (
    SELECT m.month, COUNT(rides.ride_id) AS 'accepted_rides'
    FROM months m
    LEFT JOIN  (SELECT a.ride_id, r.requested_at
                FROM AcceptedRides a
                JOIN Rides r
                ON a.ride_id = r.ride_id) rides
    ON m.month = MONTH(rides.requested_at)
    AND m.year = YEAR(rides.requested_at)
    GROUP BY m.month
)

SELECT a1.month, a1.active_drivers, a2.accepted_rides
FROM active_drivers a1
LEFT JOIN accepted_rides a2
ON a1.month = a2.month
"""

# 1645
"""
WITH RECURSIVE months AS (
    SELECT 1 AS 'month',
           2020 AS 'year'
    UNION ALL
    SELECT month + 1, year
    FROM months
    WHERE month < 12
), active_drivers AS (
    SELECT m.month, COUNT(d.driver_id) AS 'active_drivers'
    FROM months m
    LEFT JOIN Drivers d
    ON m.year > YEAR(d.join_date)
    OR (m.month >= MONTH(d.join_date) AND m.year = YEAR(d.join_date))
    GROUP BY m.month
), active_accepted_drivers AS (
    SELECT m.month, COUNT(DISTINCT rides.driver_id) AS 'accepted_drivers'
    FROM months m
    LEFT JOIN  (SELECT a.driver_id, r.requested_at
                FROM AcceptedRides a
                JOIN Rides r
                ON a.ride_id = r.ride_id) rides
    ON m.month = MONTH(rides.requested_at)
    AND m.year = YEAR(rides.requested_at)
    GROUP BY m.month
)

SELECT a1.month, CASE WHEN a1.active_drivers = 0 THEN 0
                      ELSE ROUND((a2.accepted_drivers/a1.active_drivers) * 100, 2)
                      END AS 'working_percentage'
FROM active_drivers a1
LEFT JOIN active_accepted_drivers a2
ON a1.month = a2.month
"""

# 1651
"""
WITH RECURSIVE months AS (
    SELECT 1 AS 'month',
           2020 AS 'year'
    UNION ALL
    SELECT month + 1, year
    FROM months
    WHERE month < 12
), accepted AS (
    SELECT a.ride_id, r.requested_at, a.ride_distance, a.ride_duration
    FROM AcceptedRides a
    JOIN Rides r
    ON a.ride_id = r.ride_id
), monthly AS (
    SELECT m.month, SUM(IFNULL(ac.ride_distance, 0)) AS 'month_ride_distance', SUM(IFNULL(ac.ride_duration, 0)) AS 'month_ride_duration'
    FROM months m
    LEFT JOIN accepted ac
    ON m.month = MONTH(ac.requested_at)
    AND m.year = YEAR(ac.requested_at)
    GROUP BY m.month
)

SELECT m1.month, ROUND(SUM(m2.month_ride_distance)/3, 2) AS 'average_ride_distance'
      ,ROUND(SUM(m2.month_ride_duration)/3, 2) AS 'average_ride_duration'
FROM monthly m1
LEFT JOIN monthly m2
ON m2.month - m1.month < 3
AND m2.month >= m1.month
GROUP BY m1.month
HAVING month <= 10
ORDER BY month
"""

# 1661
"""
SELECT a1.machine_id, ROUND(AVG(a1.timestamp - a2.timestamp), 3) AS 'processing_time'
FROM Activity a1
LEFT JOIN Activity a2
ON a1.machine_id = a2.machine_id
AND a1.process_id = a2.process_id
AND a1.activity_type != a2.activity_type
WHERE a1.activity_type = 'end'
GROUP BY a1.machine_id
"""

# 1667
"""
SELECT user_id, CONCAT(UPPER(LEFT(name, 1)), LOWER(SUBSTRING(name, 2))) AS 'name'
FROM Users
ORDER BY user_id ASC
"""

# 1677
"""
SELECT p.name, SUM(i.rest) AS 'rest', SUM(i.paid) AS 'paid', SUM(i.canceled) AS 'canceled', SUM(i.refunded) AS 'refunded'
FROM Invoice i
LEFT JOIN Product p
ON i.product_id = p.product_id
GROUP BY p.name
ORDER BY name ASC
"""

# 1683
"""
SELECT t.tweet_id
FROM Tweets t
WHERE LENGTH(t.content) > 15
"""

# 1693
"""
SELECT d.date_id, d.make_name, COUNT(DISTINCT d.lead_id) AS 'unique_leads', COUNT(DISTINCT d.partner_id) AS 'unique_partners'
FROM DailySales d
GROUP BY d.date_id, d.make_name
"""

# 1699
"""
SELECT c2.person1, c2.person2, COUNT(1) AS 'call_count', SUM(c2.duration) AS 'total_duration'
FROM (
    SELECT CASE WHEN c.from_id > c.to_id THEN c.to_id
                ELSE c.from_id END AS 'person1'
          ,CASE WHEN c.from_id < c.to_id THEN c.to_id
                ELSE c.from_id END AS 'person2'
          ,c.duration
    FROM Calls c
) c2
GROUP BY c2.person1, c2.person2
"""

# 1709
"""
WITH visit AS (
    SELECT u.user_id, u.visit_date, ROW_NUMBER() OVER(PARTITION BY u.user_id ORDER BY u.visit_date ASC) AS 'row_number'
    FROM UserVisits u
)

SELECT v1.user_id, MAX(DATEDIFF(CASE WHEN v2.visit_date IS NULL THEN '2021-1-1' ELSE v2.visit_date END, v1.visit_date)) AS 'biggest_window'
FROM visit v1
LEFT JOIN visit v2
ON v1.row_number + 1 = v2.row_number
AND v1.user_id = v2.user_id
GROUP BY v1.user_id
ORDER BY user_id ASC
"""

# 1715
"""
SELECT SUM(b.apple_count + IFNULL(c.apple_count, 0)) AS 'apple_count'
      ,SUM(b.orange_count + IFNULL(c.orange_count, 0)) AS 'orange_count'
FROM Boxes b
LEFT JOIN Chests c
ON b.chest_id = c.chest_id
"""

# 1729
"""
SELECT f.user_id, COUNT(1) AS 'followers_count'
FROM Followers f
GROUP BY f.user_id
ORDER BY f.user_id ASC
"""

# 1731
"""
SELECT t.employee_id, e2.name, t.reports_count, ROUND(t.average_age, 0) AS 'average_age'
FROM (
    SELECT e.reports_to AS 'employee_id', COUNT(1) AS 'reports_count', AVG(e.age) AS 'average_age'
    FROM Employees e
    WHERE e.reports_to IS NOT NULL
    GROUP BY e.reports_to
    ) t
LEFT JOIN Employees e2
ON e2.employee_id = t.employee_id
ORDER BY employee_id ASC
"""

# 1741
"""
SELECT e.event_day AS 'day', e.emp_id, SUM(e.out_time - e.in_time) AS 'total_time'
FROM Employees e
GROUP BY e.event_day, e.emp_id
"""

# 1747
"""
SELECT DISTINCT l.account_id
FROM LogInfo l
JOIN LogInfo l2
ON (l2.login BETWEEN l.login AND l.logout
OR l2.logout BETWEEN l.login AND l.logout)
AND l.account_id = l2.account_id
AND l.ip_address != l2.ip_address
"""

# 1757
"""
SELECT p.product_id
FROM Products p
WHERE p.low_fats = 'Y'
AND p.recyclable = 'Y'
"""

# 1767
"""
WITH RECURSIVE pairs AS (
    SELECT t.task_id, 1 AS 'subtask_id'
    FROM Tasks t
    UNION ALL
    SELECT p.task_id, p.subtask_id + 1 AS 'subtask_id'
    FROM pairs p
    WHERE p.subtask_id + 1 <= (SELECT t2.subtasks_count FROM Tasks t2 WHERE t2.task_id = p.task_id)
)

SELECT p.task_id, p.subtask_id
FROM pairs p
LEFT JOIN Executed e
ON p.task_id = e.task_id
AND p.subtask_id = e.subtask_id
WHERE e.task_id IS NULL
"""

# 1777
"""
SELECT p.product_id
      ,SUM(CASE WHEN p.store = 'store1' THEN p.price
            ELSE NULL END) AS 'store1'
      ,SUM(CASE WHEN p.store = 'store2' THEN p.price
            ELSE NULL END) AS 'store2'
      ,SUM(CASE WHEN p.store = 'store3' THEN p.price
            ELSE NULL END) AS 'store3'
FROM Products p
GROUP BY p.product_id
"""

# 1783
"""
WITH c AS (
    SELECT Wimbledon AS 'player_id'
    FROM Championships
    UNION ALL
    SELECT Fr_open AS 'player_id'
    FROM Championships
    UNION ALL
    SELECT US_open AS 'player_id'
    FROM Championships
    UNION ALL
    SELECT Au_open AS 'player_id'
    FROM Championships
), championships_count AS (
    SELECT c.player_id, COUNT(1) AS 'grand_slams_count'
    FROM c
    GROUP BY c.player_id
)

SELECT c2.player_id, p.player_name, c2.grand_slams_count
FROM championships_count c2
LEFT JOIN Players p
ON p.player_id = c2.player_id
"""

# 1789
"""
SELECT e.employee_id , e.department_id
FROM Employee e
WHERE e.primary_flag = 'Y'
UNION
(
    SELECT e2.employee_id , e2.department_id
    FROM Employee e2
    GROUP BY e2.employee_id
    HAVING COUNT(1) = 1
)
"""

# 1795
"""
SELECT p.product_id, 'store1' AS 'store', p.store1 AS 'price'
FROM Products p
WHERE p.store1 IS NOT NULL
UNION ALL
(
    SELECT p.product_id, 'store2' AS 'store', p.store2 AS 'price'
    FROM Products p
    WHERE p.store2 IS NOT NULL
)
UNION ALL
(
    SELECT p.product_id, 'store3' AS 'store', p.store3 AS 'price'
    FROM Products p
    WHERE p.store3 IS NOT NULL
)
"""

# 1809
"""
SELECT p.session_id
FROM Playback p
LEFT JOIN Ads a
ON a.timestamp BETWEEN p.start_time AND p.end_time
AND p.customer_id = a.customer_id
WHERE a.ad_id IS NULL
"""

# 1811
"""
WITH contest_user AS (
    SELECT c.contest_id, u.user_id
    FROM Contests c
    LEFT JOIN Users u
    ON c.gold_medal = u.user_id
    OR c.silver_medal = u.user_id
    OR c.bronze_medal = u.user_id
), contest_user_cons AS (
    SELECT c1.contest_id, c1.user_id, COUNT(1) AS 'count_consecutive'
    FROM contest_user c1
    JOIN contest_user c2
    ON c1.user_id = c2.user_id
    AND c2.contest_id BETWEEN c1.contest_id AND c1.contest_id + 2
    GROUP BY c1.contest_id, c1.user_id
    HAVING count_consecutive >= 3
), gold_count AS (
    SELECT c3.gold_medal AS 'user_id'
    FROM Contests c3
    GROUP BY c3.gold_medal
    HAVING COUNT(1) >= 3
), all_id AS (
    SELECT g.user_id
    FROM gold_count g
    UNION
    (
        SELECT c4.user_id
        FROM contest_user_cons c4
    )

)

SELECT u.name, u.mail
FROM all_id a
LEFT JOIN Users u
ON a.user_id = u.user_id
"""