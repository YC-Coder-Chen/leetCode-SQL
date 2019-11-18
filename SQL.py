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
