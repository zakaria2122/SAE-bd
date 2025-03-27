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
        # parcours du résultat de la requête. 
        # ligne peut être vu comme un dictionnaire dont les clés sont les noms des colonnes de votre requête
        # est les valeurs sont les valeurs de ces colonnes pour la ligne courante
        # par exemple ligne['numcom'] va donner le numéro de la commande de la ligne courante 
        ...

    #ici fin du traitement
    # fermeture de la requête
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
        requete=fic_req.read()
    print(faire_factures(requete,mois,annee,ms))