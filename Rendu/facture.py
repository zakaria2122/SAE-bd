import sqlalchemy
import argparse
import getpass
from sqlalchemy.sql import text

class MySQL(object):
    def __init__(self, user, passwd, host, database,timeout=20):
        self.user = user
        self.passwd = passwd
        self.host = host
        self.database = database
        #try:
        self.engine = sqlalchemy.create_engine(
                'mysql+mysqlconnector://' + self.user + ':' + self.passwd + '@' + self.host + '/' + self.database,
                )
        self.cnx = self.engine.connect()
        print("connexion réussie")

    def close(self):
        self.cnx.close()

    def execute(self, requete, liste_parametres):
        for param in liste_parametres:
            if type(param)==str:
                requete=requete.replace('?',"'"+param+"'",1)
            else:
                requete=requete.replace('?',str(param),1)
 
        requete= text(requete)
        return self.cnx.execute(requete)

    



def faire_factures(requete: str, mois: int, annee: int, bd: MySQL):
    curseur = bd.execute(requete, (mois, annee))

    res = []
    chiffre_affaire_global = 0
    total_livres_vendus_global = 0
    nombre_factures_global = 0

    magasin_actuel = None
    facture_courante = None
    total_commande = 0
    total_livres_vendus_magasin = 0
    nombre_factures_magasin = 0

    res.append(f"Factures du {mois}/{annee}")

    for ligne in curseur:
        magasin = ligne[0]
        client_nom = ligne[1]
        client_prenom = ligne[2]
        client_adresse = f"{ligne[3]}\n{ligne[4]} {ligne[5]}"
        numcom = ligne[6]
        datecom = ligne[7].strftime("%d/%m/%Y")
        isbn = ligne[8]
        titre = ligne[9]
        quantite = ligne[10]
        prix_unitaire = ligne[11]
        prix_total = ligne[12]

        chiffre_affaire_global += prix_total
        total_livres_vendus_global += quantite

        # Changement de magasin
        if magasin_actuel != magasin:
            if magasin_actuel is not None:
                # Ajouter le résumé du magasin précédent
                res.append(f"{'-' * 85}")
                res.append(f"{nombre_factures_magasin} factures éditées")
                res.append(f"{total_livres_vendus_magasin} livres vendus")
                res.append(f"{'*' * 85}")

            # Nouvelle section pour le magasin
            res.append(f"\nEdition des factures du magasin {magasin}")
            res.append(f"{'-' * 85}")

            magasin_actuel = magasin
            nombre_factures_magasin = 0
            total_livres_vendus_magasin = 0

        # Changement de facture
        if facture_courante != numcom:
            if facture_courante is not None:
                res.append(f"{'-' * 85}")
                res.append(f"Total de la commande : {total_commande:.2f} €")
                res.append(f"{'-' * 85}")

            res.append(f"\n{client_nom} {client_prenom}")
            res.append(client_adresse)
            res.append(f"Commande n°{numcom} du {datecom}")
            res.append(f"{'ISBN':<15}{'Titre':<40}{'Qte':<6}{'Prix':<10}{'Total':<10}")
            res.append(f"{'-' * 85}")

            facture_courante = numcom
            nombre_factures_magasin += 1
            nombre_factures_global += 1
            total_commande = 0

        # Ajouter la ligne de commande
        res.append(f"{isbn:<15}{titre[:40]:<40}{quantite:<6}{prix_unitaire:<10.2f}{prix_total:<10.2f}")
        total_commande += prix_total
        total_livres_vendus_magasin += quantite

    # Finalisation de la dernière commande
    if facture_courante is not None:
        res.append(f"{'-' * 85}")
        res.append(f"Total de la commande : {total_commande:.2f} €")
        res.append(f"{'-' * 85}")

    # Ajout du dernier résumé de magasin
    if magasin_actuel is not None:
        res.append(f"{'-' * 85}")
        res.append(f"{nombre_factures_magasin} factures éditées")
        res.append(f"{total_livres_vendus_magasin} livres vendus")
        res.append(f"{'*' * 85}")

    # Résumé global
    res.append(f"\n{'*' * 85}")
    res.append(f"Chiffre d’affaire global: {chiffre_affaire_global:.2f} €")
    res.append(f"Nombre total de livres vendus: {total_livres_vendus_global}")
    res.append(f"{'*' * 85}")

    curseur.close()
    return "\n".join(res)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--serveur",dest="nomServeur", help="Nom ou adresse du serveur de base de données", type=str, default="servinfo-maria")
    parser.add_argument("--bd",dest="nomBaseDeDonnees", help="Nom de la base de données", type=str,default='Librairie')
    parser.add_argument("--login",dest="nomLogin", help="Nom de login sur le serveur de base de donnée", type=str, default='moins')
    parser.add_argument("--requete", dest="fichierRequete", help="Fichier contenant la requete des commandes", type=str , default='fic_req.sql')    
    args = parser.parse_args()
    passwd = getpass.getpass("mot de passe SQL:")
    try:
        ms = MySQL(args.nomLogin, passwd, args.nomServeur, args.nomBaseDeDonnees)
    except Exception as e:
        print("La connection a échoué avec l'erreur suivante:", e)
        exit(0)
    rep=input("Entrez le mois et l'année sous la forme mm/aaaa ")
    mm,aaaa=rep.split('/')
    mois=int(mm)
    annee=int(aaaa)
    with open(args.fichierRequete) as fic_req:
        requete=fic_req.read()
    print(faire_factures(requete,mois,annee,ms))