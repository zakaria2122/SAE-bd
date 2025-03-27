SELECT
    nommag AS nom_magasin,
    nomcli AS client_nom,
    prenomcli AS client_prenom,
    adressecli AS client_adresse,
    codepostal AS client_code_postal,
    villecli AS client_ville,
    numcom AS id_commande,
    datecom AS date_commande,
    isbn,
    titre,
    qte AS quantite,
    prixvente AS prix,
    (qte * prixvente) AS total_ligne,
    total_commande
FROM
    MAGASIN
NATURAL JOIN COMMANDE
NATURAL JOIN CLIENT
NATURAL JOIN DETAILCOMMANDE
NATURAL JOIN LIVRE
NATURAL JOIN (
    SELECT
        numcom,
        SUM(qte * prixvente) AS total_commande
    FROM
        DETAILCOMMANDE
    NATURAL JOIN LIVRE
    GROUP BY
        numcom
) AS total
WHERE
    MONTH(datecom) = ?
    AND YEAR(datecom) = ?
ORDER BY
    nommag, datecom, numcom
