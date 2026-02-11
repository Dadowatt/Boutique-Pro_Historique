import mysql.connector
import hashlib
import re

# Connexion à la base de données
connexion = mysql.connector.connect(
    host='localhost',
    user='root',
    password='watt123',
    database='boutique_pro_historique',
    port=3307
)
curseur = connexion.cursor(dictionary=True)
print("Connecté à la base de donnée MySQL")

#gestion des catégories
def ajouter_categorie():
    try:
        while True:
            nom_categorie = input("Nom de la catégorie à ajouter : ").lower().strip()
            if nom_categorie.replace(" ", "").isalpha():
                break
            print("Le nom de la catégorie doit contenir uniquement des lettres")

        sql = "INSERT INTO categories (nom_categorie) VALUES(%s)"
        curseur.execute(sql, (nom_categorie,))
        connexion.commit()
        print(f"Catégorie {nom_categorie} ajoutée avec succès !")

    except mysql.connector.Error as e:
        print(f"Erreur MySQL : {e}")

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

#gestion des produits
def ajouter_produit():
    try:
        while True:
            try:
                designation = input("Saisir le nom du produit : ").strip()
                if designation.replace(" ", "").isalpha():
                    break
                print("Le nom doit contenir uniquement des lettres")
            except ValueError:
                print("Veuillez un nom de produit valide")

        while True:
            try:
                prix = float(input("Saisir le prix du produit : "))
                if prix >= 0:
                    break
                print("Le prix doit être positif")
            except ValueError:
                print("Veuillez entrer un nombre valide")
        while True:
            try:
                stock = int(input("Saisir le stock initial : "))
                if stock >= 0:
                    break
                print("Le stock doit être positif")
            except ValueError:
                print("Veuillez entrer un nombre entier")

        # Afficher les catégories
        sql_cat = "SELECT * FROM categories"
        curseur.execute(sql_cat)
        categories = curseur.fetchall()

        if not categories:
            print("Aucune catégorie disponible. veuillez ajouter d'abord une catégorie")
            return
        print("\nListe des catégories :")
        for c in categories:
            print(f"ID: {c['id']} | Nom: {c['nom_categorie']}")

        categorie_id = int(input("Choisis l'ID de la catégorie du produit : "))

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
        if not produits:
            print("Aucun produit disponible")
            return
        for p in produits:
            print(f"ID: {p['id']} | Nom: {p['designation']} | Stock: {p['stock']}")
        
        while True:
            try:
                id_produit = int(input("Choisis l'ID du produit : "))
                if any(p['id'] == id_produit for p in produits):
                    break
                print("ID produit inexistant, veuillez ressayer")
            except ValueError:
                print("Veuillez saisir un nombre entier valide pour l'ID")

        while True:
            try:
                quantite = int(input("Quantité à ajouter/retirer : "))
                if quantite > 0:
                    break
                else:
                    print("La quantité doit être positive")
            except ValueError:
                print("Veuillez saisir un nombre entier valide pour la quantité")
        
        while True:
            type_mouvement = input("Type de mouvement (ENTREE/SORTIE) : ").upper()
            if type_mouvement in ["ENTREE", "SORTIE"]:
                break
            print("Type de mouvement invalide ! veuillez ressayer")    

        # Récupérer le stock actuel
        sql_stock = "SELECT stock FROM produits WHERE id=%s"
        curseur.execute(sql_stock, (id_produit,))
        ligne = curseur.fetchone()
        if ligne is None:
            print("Produit introuvable")
            return
        
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
        update_stock = "UPDATE produits SET stock=%s WHERE id=%s"
        curseur.execute(update_stock, (nouveau_stock, id_produit))
        connexion.commit()
        print(f"Mouvement effectué. Nouveau stock pour le produit {id_produit} : {nouveau_stock}")

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

#gestion inscription
def inscrire_utilisateur():
    try:
        while True:
            email = input("Email : ").strip()

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                print("Format d'email invalide.")
                continue
            break

        while True:
            password = input("Mot de passe : ").strip()
            if len(password) < 4:
                print("Le Mot de passe doit contenir au minimum 4 caractères")
                continue
            break

        #hashage du mot de passe
        hash_password = hashlib.sha256(password.encode()).hexdigest()
        role = 'user'

        sql = """
        INSERT INTO utilisateurs (email, mot_de_passe, role)
        VALUES (%s, %s, %s)
        """
        curseur.execute(sql, (email, hash_password, role))
        connexion.commit()

        print("Utilisateur créé avec succès !")
    except mysql.connector.IntegrityError:
        print("Cet email est déjà utilisé.")
    except mysql.connector.Error as e:
        print(f"Erreur MySQL : {e}")

#gestion connexion
def login():
    try:
        email = input("email : ").strip()
        password = input("Mot de pass : ").strip()

        sql = "SELECT * FROM utilisateurs WHERE email=%s"
        curseur.execute(sql, (email,))
        user = curseur.fetchone()

        if user:
            hash_tape = hashlib.sha256(password.encode()).hexdigest()
        if hash_tape == user['mot_de_passe']:
                print(f"\nBienvenue {email} !")
                return user
        
        print("Identifiant incorrect\n")
        return None

    except mysql.connector.Error as e:
        print(f"Erreur mySQL : {e}")
        return None

# Menu principal
while True:
    print("\n=== Bienvenue dans Boutique-Pro & Historique ===")
    print("1. S'inscrire")
    print("2. Se connecter")
    print("9. Quitter")

    choix_init = input("Choisissez une option : ").strip()

    if choix_init == "1":
        inscrire_utilisateur()
    elif choix_init == "2":
        utilisateur_connecte = None
        while not utilisateur_connecte:
            utilisateur_connecte = login()

        # affichage du menu adapté après connexion réussie
        role = utilisateur_connecte['role']
        email_connecte = utilisateur_connecte['email']

        while True:
            print(f"\n=== Menu Boutique-Pro & Historique (connecté : {email_connecte}, rôle : {role})")
            print("2. Lister les catégories")
            print("4. Lister les produits")
            print("6. Produits avec stock < 5")

            # Options réservées à l'admin
            if role == "admin":
                print("1. Ajouter une catégorie")
                print("3. Ajouter un produit")
                print("5. Ajouter ou Retirer stock")

            print("0. Déconnexion")
            print("9. Quitter le programme")

            choix = input("Saisir votre choix : ").strip()

            if choix == "2":
                afficher_categorie()
            elif choix == "4":
                lister_produits()
            elif choix == "6":
                alerte_stock()

            # Options accessibles uniquement à l'admin
            elif choix == "1" and role == "admin":
                ajouter_categorie()
            elif choix == "3" and role == "admin":
                ajouter_produit()
            elif choix == "5" and role == "admin":
                ajouter_mouvement()

            elif choix == "0":
                print("Déconnexion...\n")
                break

            elif choix == "9":
                print("Au revoir !")
                curseur.close()
                connexion.close()
                exit()
            else:
                print("Choix invalide, veuillez réessayer.")

    elif choix_init == "9":
        print("Au revoir !")
        curseur.close()
        connexion.close()
        break
    else:
        print("Choix invalide, veuillez réessayer.")



