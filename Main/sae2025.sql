-- Devoir 127
-- Nom: MOINS, MAKHLOUF , Prenom: Bastien


-- Feuille SAE2.05 Exploitation d'une base de données: Livre Express
--
-- Veillez à bien répondre aux emplacements indiqués.
-- Seule la première requête est prise en compte.


-- +-----------------------+--
-- * Question 127156 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Quels sont les livres qui ont été commandés le 1er décembre 2024 ?


-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +---------------+--------------------------------------------+---------+-----------+-------+
-- | isbn          | titre                                      | nbpages | datepubli | prix  |
-- +---------------+--------------------------------------------+---------+-----------+-------+
-- | etc...
-- = Reponse question 127156.


select distinct  isbn, titre, nbpages, datepubli, prix
from CLIENT natural join COMMANDE natural join LIVRE natural join AUTEUR natural join ECRIRE natural join DETAILCOMMANDE


where datecom = '2024-12-01'
order by titre;






-- +-----------------------+--
-- * Question 127202 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Quels clients ont commandé des livres de René Goscinny en 2021 ?


-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+---------+-----------+-----------------------------+------------+-------------+
-- | idcli | nomcli  | prenomcli | adressecli                  | codepostal | villecli    |
-- +-------+---------+-----------+-----------------------------+------------+-------------+
-- | etc...
-- = Reponse question 127202.
select distinct idcli, nomcli, prenomcli, adressecli, codepostal, villecli 
from CLIENT natural join COMMANDE natural join LIVRE natural join AUTEUR natural join ECRIRE natural join DETAILCOMMANDE
where YEAR(dateCom)=2021 and nomauteur = 'René Goscinny'
order by nomcli, prenomcli;


-- +-----------------------+--
-- * Question 127235 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Quels sont les livres sans auteur et étant en stock dans au moins un magasin en quantité strictement supérieure à 8 ?


-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +---------------+-----------------------------------+-------------------------+-----+
-- | isbn          | titre                             | nommag                  | qte |
-- +---------------+-----------------------------------+-------------------------+-----+
-- | etc...
-- = Reponse question 127235.
select distinct isbn, titre, nommag, qte
from POSSEDER natural join MAGASIN natural join LIVRE
where isbn not in (
   select isbn
   from ECRIRE
) and qte > 8
order by titre, nommag;






-- +-----------------------+--
-- * Question 127279 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Pour chaque magasin, on veut le nombre de clients qui habitent dans la ville de ce magasin (en affichant les 0)


-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+-------------------------+-------+
-- | idmag | nommag                  | nbcli |
-- +-------+-------------------------+-------+
-- | etc...
-- = Reponse question 127279.

select idmag, nommag, IFNULL(COUNT(DISTINCT idcli),0) AS nbcli
from MAGASIN 
natural left join COMMANDE natural left join CLIENT 
where CLIENT.villecli = MAGASIN.villemag
group by idmag, nommag;





-- +-----------------------+--
-- * Question 127291 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Pour chaque magasin, on veut la quantité de livres achetés le 15/09/2022 en affichant les 0.


-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------------------+------+
-- | nommag                  | nbex |
-- +-------------------------+------+
-- | etc...
-- = Reponse question 127291.
select nommag, sum(IFNULL(qte,0)) as nbex
from MAGASIN natural left join COMMANDE natural  join DETAILCOMMANDE
where datecom = '2022-09-15'
group by nommag;






-- +-----------------------+--
-- * Question 127314 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Instructions d'insertion dans la base de données


-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +------------+
-- | insertions |
-- +------------+
-- | etc...
-- = Reponse question 127314.

insert into LIVRE values ('9782844273765', 'SQL pour les Nuls', 292, 2002, 33.5);
insert into AUTEUR values ('OL246259A', 'Taylor Allen G.', NULL, NULL);
insert into AUTEUR values ('OL7670824A', 'Engel Reinhard', NULL, NULL);
insert into POSSEDER values (7, '9782844273765', 3);


-- +-----------------------+--
-- * Question 127369 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 1 Nombre de livres vendus par magasin et par an


-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------------------+-------+-----+
-- | Magasin                 | Année | qte |
-- +-------------------------+-------+-----+
-- | etc...
-- = Reponse question 127369.
select distinct nommag as Magasin,year(datecom) as Année, sum(qte)
from MAGASIN natural join COMMANDE natural join DETAILCOMMANDE
group by Magasin, Année
order by Magasin, Année;




-- +-----------------------+--
-- * Question 127370 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 2  Chiffre d'affaire par thème en 2024


-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +--------------------------------------+---------+
-- | Theme                                | Montant |
-- +--------------------------------------+---------+
-- | etc...
-- = Reponse question 127370.
--https://sql.sh/cours/case


     SELECT  case      WHEN LEFT(iddewey, 1) = '0' THEN 'Informatique, généralités'
       WHEN LEFT(iddewey, 1) = '1' THEN 'Philosophie et psychologie'
       WHEN LEFT(iddewey, 1) = '2' THEN 'Religion'
       WHEN LEFT(iddewey, 1) = '3' THEN 'Sciences sociales'
       WHEN LEFT(iddewey, 1) = '4' THEN 'Langues'
       WHEN LEFT(iddewey, 1) = '5' THEN 'Sciences naturelles et mathématiques'
       WHEN LEFT(iddewey, 1) = '6' THEN 'Technologie et sciences appliquées'
       WHEN LEFT(iddewey, 1) = '7' THEN 'Arts et loisirs'
       WHEN LEFT(iddewey, 1) = '8' THEN 'Littérature'
       WHEN LEFT(iddewey, 1) = '9' THEN 'Histoire et géographie'end AS Theme, SUM(prixvente * qte) AS Montant
FROM CLASSIFICATION NATURAL  JOIN THEMES NATURAL  JOIN LIVRE natural  join DETAILCOMMANDE NATURAL JOIN COMMANDE
WHERE YEAR(datecom) = '2024' 
GROUP BY theme ;


-- +-----------------------+--
-- * Question 127381 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 3 Evolution chiffre d'affaire par magasin et par mois en 2024


-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +------+-------------------------+---------+
-- | mois | Magasin                 | CA      |
-- +------+-------------------------+---------+
-- | etc...
-- = Reponse question 127381.
select distinct MONTH(datecom) as mois, nommag as Magasin, sum(prixvente*qte) as CA
from MAGASIN natural join COMMANDE natural join DETAILCOMMANDE
where YEAR(datecom) = '2024'
group by Magasin, mois;




-- +-----------------------+--
-- * Question 127437 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 4 Comparaison ventes en ligne et ventes en magasin


-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+------------+---------+
-- | annee | typevente  | montant |
-- +-------+------------+---------+
-- | etc...
-- = Reponse question 127437.


select YEAR(datecom) as annee, case
when enligne = 'O' then 'En ligne'
else 'En magasin'
end as
 typevente, sum(prixvente * qte) as montant
from COMMANDE natural join DETAILCOMMANDE
group by annee, typevente;


-- +-----------------------+--
-- * Question 127471 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 5


-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------------+-----------+
-- | Editeur           | nbauteurs |
-- +-------------------+-----------+
-- | etc...
-- = Reponse question 127471.
select distinct nomedit as Editeur, count(idauteur) as nbauteurs
from EDITEUR natural join EDITER natural join LIVRE natural join ECRIRE natural join AUTEUR
group by nomedit
order by nbauteurs desc
limit 10;


-- +-----------------------+--
-- * Question 127516 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 6 Origine des clients ayant acheter des livres de R. Goscinny


-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------+-----+
-- | ville       | qte |
-- +-------------+-----+
-- | etc...
-- = Reponse question 127516.
select distinct villecli as ville, sum(qte) as qte
from CLIENT natural join COMMANDE natural join LIVRE natural join AUTEUR natural join ECRIRE natural join DETAILCOMMANDE
where nomauteur = 'René Goscinny'
group by ville;




-- +-----------------------+--
-- * Question 127527 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 7 Valeur du stock par magasin
-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------------------+---------+
-- | Magasin                 | total   |
-- +-------------------------+---------+
-- | etc...
-- = Reponse question 127527.
select distinct nommag as Magasin, sum(prix*qte) as total
from MAGASIN natural join POSSEDER natural join LIVRE
group by Magasin;


-- +-----------------------+--
-- * Question 127538 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
-- Requête Graphique 8 Statistiques sur l'évolution du chiffre d'affaire total par client
-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+---------+---------+---------+
-- | annee | maximum | minimum | moyenne |
-- +-------+---------+---------+---------+
-- | etc...
-- = Reponse question 127538.




with TotalCa as (
   select YEAR(datecom) as annee, sum(prixvente*qte) as total
   from CLIENT natural join COMMANDE natural join DETAILCOMMANDE
   group by idcli, annee
)
select distinct idcli, annee, max(total) as maximum, min(total) as minimum, avg(total) as moyenne
from TotalCa
group by idcli, annee
order by annee;


-- +-----------------------+--
-- * Question 127572 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Palmarès


-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+-----------------------+-------+
-- | annee | nomauteur             | total |
-- +-------+-----------------------+-------+
-- | etc...
-- = Reponse question 127572.
WITH AnneeTotal AS (
   SELECT YEAR(datecom) AS annee, nomauteur, SUM(qte) AS total
   FROM COMMANDE NATURAL JOIN DETAILCOMMANDE NATURAL JOIN LIVRE NATURAL JOIN AUTEUR NATURAL JOIN ECRIRE
   WHERE YEAR(datecom) != 2025
   GROUP BY annee, nomauteur
)
select distinct at1.annee, at1.nomauteur, at1.total
from AnneeTotal at1
where total = (select max(at2.total) from AnneeTotal at2 where at2.annee = at1.annee)
order by annee asc;


-- +-----------------------+--
-- * Question 127572 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête imprimer les commandes en considérant que l'on veut celles de février 2020


-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+-----------------------+-------+
-- | annee | nomauteur             | total |
-- +-------+-----------------------+-------+
-- | etc...
-- = Reponse question 127572.
select YEAR(datecom) as annee, nomauteur, SUM(qte) as total
FROM COMMANDE NATURAL JOIN DETAILCOMMANDE NATURAL JOIN LIVRE NATURAL JOIN AUTEUR NATURAL JOIN ECRIRE
where YEAR(datecom) = 2020 and MONTH(datecom) = 2
GROUP BY annee, nomauteur
order by datecom;




