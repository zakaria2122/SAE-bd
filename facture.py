import sqlalchemy
import argparse
import getpass

from sqlalchemy import text

class MySQL(object):
    def __init__(self, user, passwd, host, database, timeout=20):
        self.user = user
        self.passwd = passwd
        self.host = host
        self.database = database
        self.engine = sqlalchemy.create_engine(
            f'mysql+mysqlconnector://{self.user}:{self.passwd}@{self.host}/{self.database}',
        )
        self.cnx = self.engine.connect()
        print("connexion réussie")

    def close(self):
        self.cnx.close()

    def execute(self, requete, liste_parametres):
        # Remplacer les "?" par les paramètres dans la requête
        for param in liste_parametres:
            if isinstance(param, str):
                requete = requete.replace('?', f"'{param}'", 1)
            else:
                requete = requete.replace('?', str(param), 1)
        # Exécuter la requête modifiée
        requete = text(requete)
        return self.cnx.execute(requete)

    


def faire_factures(requete:str, mois:int, annee:int, bd:MySQL):

    curseur=bd.execute(requete,(mois,annee))

    # Initialisation des variables
    res = []
    chiffre_affaire_global = 0
    total_livres_vendus_global = 0
    nombre_factures_global = 0
    magasin_actuel = None
    facture_courante = None
    total_commande = 0
    total_livres_vendus_magasin = 0
    nombre_factures_magasin = 0

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

        # Accumulation correcte des totaux
        chiffre_affaire_global += prix_total
        total_livres_vendus_global += quantite

        # Si on change de magasin, on affiche le résumé du précédent et on réinitialise les compteurs
        if magasin_actuel != magasin:
            if magasin_actuel is not None:
                res.append(f"\n{'-' * 85}")
                res.append(f"Résumé du magasin {magasin_actuel} :")
                res.append(f"  - {nombre_factures_magasin} factures éditées")
                res.append(f"  - {total_livres_vendus_magasin} livres vendus")
                res.append(f"{'-' * 85}")

            res.append(f"\nEdition des factures du magasin {magasin}")
            res.append(f"{'-' * 85}")
            magasin_actuel = magasin
            nombre_factures_magasin = 0
            total_livres_vendus_magasin = 0

        # Si on change de commande, on affiche la facture précédente et on en commence une nouvelle
        if facture_courante != numcom:
            if facture_courante is not None:
                res.append(f"\n{'-' * 85}")
                res.append(f"Total de la commande : {total_commande:.2f} €")
                res.append(f"{'-' * 85}")

            res.append(f"\n{client_nom} {client_prenom}")
            res.append(f"{client_adresse}")
            res.append(f"Commande n°{numcom} du {datecom}")
            res.append(f"{'ISBN':<10} {'Titre':<40} {'Qte':<6} {'Prix Unitaire':<15} {'Total':>10}")
            res.append(f"{'-' * 85}")
            facture_courante = numcom
            nombre_factures_magasin += 1
            nombre_factures_global += 1
            total_commande = 0  # Réinitialiser le total de la commande pour chaque nouvelle commande

        # Ajout de la ligne de commande
        res.append(f"{isbn:<10} {titre[:40]:<40} {quantite:<6} {prix_unitaire:<15.2f} {prix_total:<15.2f}")
        total_commande += prix_total
        total_livres_vendus_magasin += quantite

    # Finalisation de la dernière facture
    if facture_courante is not None:
        res.append(f"\n{'-' * 85}")
        res.append(f"Total de la commande : {total_commande:.2f} €")
        res.append(f"{'-' * 85}")

    # Ajout du résumé du dernier magasin
    if magasin_actuel is not None:
        res.append(f"\nRésumé du magasin {magasin_actuel} :")
        res.append(f"  - {nombre_factures_magasin} factures éditées")
        res.append(f"  - {total_livres_vendus_magasin} livres vendus")
        res.append(f"{'-' * 85}")

    # Ajout du résumé global
    res.append(f"\n{'*' * 85}")
    res.append(f"Chiffre d’affaire global: {chiffre_affaire_global:.2f} €")
    res.append(f"Nombre de livres vendus: {total_livres_vendus_global}")
    res.append(f"{'*' * 85}")

    # Fermeture du curseur et retour du résultat
    curseur.close()
    return "\n".join(res)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--serveur", dest="nomServeur", help="Nom ou adresse du serveur de base de données", type=str, default="servinfo-maria")

    parser.add_argument("--bd",dest="nomBaseDeDonnees", help="Nom de la base de données", type=str,default='Librairie')
    parser.add_argument("--login",dest="nomLogin", help="Nom de login sur le serveur de base de donnée", type=str, default='makhlouf')
    parser.add_argument("--requete", dest="fichierRequete", help="Fichier contenant la requete des commandes", type=str, default='fic_req.sql')  
    args = parser.parse_args()
    
    # Demande de mot de passe
    passwd = getpass.getpass("Mot de passe SQL : ")
    
    try:
        ms = MySQL(args.nomLogin, passwd, args.nomServeur, args.nomBaseDeDonnees)
    except Exception as e:
        print("La connexion a échoué avec l'erreur suivante:", e)
        exit(0)
    
    # Demander à l'utilisateur d'entrer le mois et l'année
    rep = input("Entrez le mois et l'année sous la forme mm/aaaa : ")
    mm, aaaa = rep.split('/')

    mois = int(mm)
    annee = int(aaaa)
    
    # Lire la requête depuis le fichier
    with open(args.fichierRequete) as fic_req:
        requete = fic_req.read()
    
    # Afficher le résultat de la fonction
    print(faire_factures(requete, mois, annee, ms))
    ms.close()
