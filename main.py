import mysql.connector
import hashlib

# Connexion à la base de données
connexion = mysql.connector.connect(
    host='localhost',
    user='root',
    password='tresbienmerci',
    database='boutique_pro_historique',
    # port=3307
)
curseur = connexion.cursor(dictionary=True)
print("Connecté à la base de donnée MySQL")

#gestion des catégories
def ajouter_categorie():
    try:
        while True:
            nom_categorie = input("Nom de la catégorie : ").lower().strip()
            if nom_categorie.replace(" ", "").isalpha():
                break
            print("Le nom de la catégorie doit contenir uniquement des lettres")

        sql = "INSERT INTO categories (nom_categorie) VALUES(%s)"
        curseur.execute(sql, (nom_categorie,))
        connexion.commit()
        print("Catégorie ajoutée avec succès !")

    except mysql.connector.Error as e:
        print(f"Erreur MySQL : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")


def afficher_categorie():
    try:
        sql = "SELECT * FROM categories"
        curseur.execute(sql)
        resultats = curseur.fetchall()
        if resultats:
            print("\nListe des catégories :")
            print(f"-"*30)
            for c in resultats:
                print(f"ID: {c['id']} | Nom: {c['nom_categorie']}")
        else:
            print("Aucune catégorie trouvée.")
    except mysql.connector.Error as e:
        print(f"Erreur MySQL : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

#gestion des produits
def ajouter_produit():
    try:
        designation = input("Nom du produit : ").strip()
        prix = float(input("Prix du produit : "))
        stock = int(input("Stock initial : "))

        # Afficher les catégories
        sql_cat = "SELECT * FROM categories"
        curseur.execute(sql_cat)
        categories = curseur.fetchall()
        for c in categories:
            print(f"ID: {c['id']} | Nom: {c['nom_categorie']}")
        categorie_id = int(input("Choisis l'ID de la catégorie : "))

        # Ajout du produit
        sql_produit = """
            INSERT INTO produits (designation, prix, stock, categorie_id)
            VALUES (%s, %s, %s, %s)
        """
        curseur.execute(sql_produit, (designation, prix, stock, categorie_id))
        connexion.commit()

        # Récupéreration de l'ID du produit ajouté
        id_produit = curseur.lastrowid

        # Ajout du mouvement initial entrée
        sql_mouvement = """
            INSERT INTO mouvements (id_produit, quantite, type_mouvement, date_mouvement)
            VALUES (%s, %s, 'ENTREE', NOW())
        """
        curseur.execute(sql_mouvement, (id_produit, stock))
        connexion.commit()

        print("Produit ajouté avec succès avec stock initial !")

    except mysql.connector.Error as e:
        print(f"Erreur MySQL : {e}")
    except ValueError:
        print("Erreur : le prix et le stock doivent être des nombres.")
    except Exception as e:
        print(f"Erreur inattendue : {e}")


def lister_produits():
    try:
        sql = """
            SELECT p.id, p.designation, p.prix, p.stock, c.nom_categorie
            FROM produits p
            JOIN categories c ON p.categorie_id = c.id
        """
        curseur.execute(sql)
        produits = curseur.fetchall()
        if produits:
            print("\nListe des produits :")
            print(f"-"*75)
            for p in produits:
                print(f"ID: {p['id']} | Nom: {p['designation']} | Prix: {p['prix']} | Stock: {p['stock']} | Catégorie: {p['nom_categorie']}")
        else:
            print("Aucun produit trouvé.")
    except mysql.connector.Error as e:
        print(f"Erreur MySQL : {e}")

#gestion des mouvements
def ajouter_mouvement():
    try:
        # Afficher les produits
        sql_produits = "SELECT * FROM produits"
        curseur.execute(sql_produits)
        produits = curseur.fetchall()
        for p in produits:
            print(f"ID: {p['id']} | Nom: {p['designation']} | Stock: {p['stock']}")
        id_produit = int(input("Choisis l'ID du produit : "))

        # Demander la quantité et le type
        quantite = int(input("Quantité à ajouter/retirer : "))
        type_mouvement = input("Type de mouvement (ENTREE/SORTIE) : ").upper()
        if type_mouvement not in ["ENTREE", "SORTIE"]:
            print("Type de mouvement invalide !")
            return

        # Récupérer le stock actuel
        sql_stock = "SELECT stock FROM produits WHERE id=%s"
        curseur.execute(sql_stock, (id_produit,))
        ligne = curseur.fetchone()
        stock_actuel = ligne["stock"]

        # Calculer le nouveau stock
        if type_mouvement == "ENTREE":
            nouveau_stock = stock_actuel + quantite
        else:
            nouveau_stock = stock_actuel - quantite

        if nouveau_stock < 0:
            print("Erreur : stock insuffisant !")
            return

        # Mettre à jour le stock
        sql_update_stock = "UPDATE produits SET stock=%s WHERE id=%s"
        curseur.execute(sql_update_stock, (nouveau_stock, id_produit))
        connexion.commit()

        # Ajouter le mouvement dans la table mouvements
        sql_mouvement = """
            INSERT INTO mouvements (id_produit, quantite, type_mouvement, date_mouvement)
            VALUES (%s, %s, %s, NOW())
        """
        curseur.execute(sql_mouvement, (id_produit, quantite, type_mouvement))
        connexion.commit()

        print(f"Mouvement {type_mouvement} enregistré avec succès !")

    except mysql.connector.Error as e:
        print(f"Erreur MySQL : {e}")
    except ValueError:
        print("Erreur : l'ID et la quantité doivent être des nombres.")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

#Alerte stock faible
def alerte_stock():
    try:
        sql = """
            SELECT p.id, p.designation, p.stock, c.nom_categorie
            FROM produits p
            JOIN categories c ON p.categorie_id = c.id
            WHERE p.stock < 5
        """
        curseur.execute(sql)
        produits = curseur.fetchall()
        if produits:
            print("\n Produits avec stock inférieur à 5 :")
            print(f"-"*60)
            for p in produits:
                print(f"ID: {p['id']} | Nom: {p['designation']} | Stock: {p['stock']} | Catégorie: {p['nom_categorie']}")
        else:
            print("Tous les produits ont un stock suffisant.")
    except mysql.connector.Error as e:
        print(f"Erreur MySQL : {e}")

#Fonction pour hasher mes mot de passe
def hasher_mot_de_passe(mot_de_passe):
    return hashlib.sha256(mot_de_passe.encode()).hexdigest()


#fonction inscription
def inscription():
    try:
        print("\n=== Inscription ===")
        email = input("Entrer votre Email : ").strip()

        # Vérifier si l'email existe déjà
        sql = "SELECT id FROM utilisateurs WHERE email = %s"
        curseur.execute(sql, (email,))
        if curseur.fetchone():
            print("Cet email est déjà utilisé")
            return False

        mot_de_passe = input("Entrer votre Mot de passe : ").strip()

        # Hashage du mot de passe
        mot_de_passe_hash = hasher_mot_de_passe(mot_de_passe)

        sql = """
            INSERT INTO utilisateurs (email, mot_de_passe, role)
            VALUES (%s, %s, 'utilisateur')
        """
        curseur.execute(sql, (email, mot_de_passe_hash))
        connexion.commit()

        print("Inscription réussie")
        return True

    except Exception as e:
        print(f"Erreur MySQL : {e}")
        return False


#fonction pour l'authentification
def connexions():
    try:
        print("\n=== Connexion ===")
        email = input("Entrer votre email : ").strip()
        mot_de_passe = input("Entrer votre mot de passe : ").strip()

        mot_de_passe_hash = hasher_mot_de_passe(mot_de_passe)

        sql = """
            SELECT id, email, role
            FROM utilisateurs
            WHERE email = %s AND mot_de_passe = %s
        """
        curseur.execute(sql, (email, mot_de_passe_hash))
        utilisateur = curseur.fetchone()

        if utilisateur:
            print(f"Connexion réussie (rôle : {utilisateur['role']})")
            return utilisateur
        else:
            print("Email ou mot de passe incorrect")
            return None

    except Exception as e:
        print(f"Erreur MySQL : {e}")
        return None




def authentification():
    while True:
        print("\n=== Authentification ===")
        print("1. Se connecter")
        print("2. S'inscrire")
        print("0. Quitter")
        choix = input("Choisissez une option : ")

        if choix == "1":
            utilisateur = connexions()
            if utilisateur:
                return utilisateur
        elif choix == "2":
            inscription()
        elif choix == "0":
            print("Au revoir !")
            exit()
        else:
            print("Choix invalide")





utilisateur_connecte = authentification()
role = utilisateur_connecte["role"]

# Menu principal
while True:
    print("\n=== Menu Boutique-Pro & Historique ===")
    print("1. Lister les catégories")
    print("2. Lister les produits")

    if role == "admin":
        print("3. Ajouter une catégorie")
        print("4. Ajouter un produit")
        print("5. Ajouter ou Retirer stock")

    print("6. Produits avec stock < 5")
    print("0. Quitter")

    choix = input("Saisir votre choix : ")

    if choix == "1":
        afficher_categorie()
    elif choix == "2":
        lister_produits()
    elif choix == "3" and role == "admin":
        ajouter_categorie()
    elif choix == "4" and role == "admin":
        ajouter_produit()
    elif choix == "5" and role == "admin":
        ajouter_mouvement()
    elif choix == "6":
        alerte_stock()
    elif choix == "0":
        print("Déconnexion")
        break
    else:
        print("Accès refusé ou choix invalide")


# Fermeture de la connexion
curseur.close()
connexion.close()
