DECLARE @topFolder_id int = [INPUT FOLDER ID]

DECLARE @table TABLE
(
[document_id] int,
[document_name] nvarchar(450),
[type] int,
[folder_id] int,
[path] nvarchar(450),
[level] int
)

; WITH cteAnchor (document_id, pname, level) AS (
SELECT latest_document.document_id
, document_revision.name AS pname
, 1 AS level
FROM latest_document
INNER JOIN document_revision ON document_revision.document_id = latest_document.document_id
AND latest_document.document_id = @topFolder_id
WHERE document_revision.document_version = latest_document.document_version

UNION ALL

SELECT sub_document.sub_document_id
, cast(anchor.pname + ' > ' + latest_document_full.name AS NVARCHAR(200)) AS pname
, level + 1
FROM sub_document
INNER JOIN latest_document_full ON sub_document.sub_document_id = latest_document_full.document_id
INNER JOIN cteAnchor AS anchor ON sub_document.document_id = anchor.document_id
WHERE latest_document_full.type = 4
)


INSERT @table
(
[document_id],
[document_name],
[type],
[folder_id],
[path],
[level]
)

SELECT DISTINCT sub_document.sub_document_id AS document_id
, document_revision.name AS document_name
, document_revision.type
, sub_document.document_id AS folder_id
, pname AS path
, level
FROM cteAnchor
INNER JOIN sub_document ON cteAnchor.document_id = sub_document.document_id
INNER JOIN document_revision ON document_revision.document_id = sub_document.sub_document_id
INNER JOIN latest_document_full ldf ON ldf.document_id = document_revision.document_id AND ldf.document_version = document_revision.document_version

SELECT DISTINCT a.document_id,
d.document_name,
d.path,
COALESCE((SELECT cp.login FROM current_person cp WHERE cp.person_id=a.person_id), 'DELETED USER') AS 'login',
(SELECT count(al.analytic_log_id) from analytic_log al where al.document_id=a.document_id and al.person_id=a.person_id and time >= 'YYYY-MM-DD 00:00:00' and time <= 'YYYY-MM-DD 00:00:00') as 'accesses',
p.firstname,
p.lastname,
a.time as 'Last Access Date',
u.roles
FROM analytic_log a join person p on a.person_id=p.person_id join user_roles u on u.person_id = p.person_id
inner join @table d on d.document_id=a.document_id
WHERE time >= 'YYYY-MM-DD 00:00:00' and time <= 'YYYY-MM-DD 00:00:00'

GROUP BY a.document_id, d.path, d.document_name, a.person_id, p.firstname, p.lastname, a.time, a.analytic_log_id, u.roles
ORDER BY a.document_id ASC, 'accesses' DESC
