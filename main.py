import mysql.connector

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
            try:
                nom_categorie = input("Nom de la catégorie à ajouter : ").lower().strip()
                if nom_categorie.replace(" ", "").isalpha():
                    break
                print("Le nom de la catégorie doit contenir uniquement des lettres")
            except ValueError:
                print("Veuillez entrer uniquement des lettres")

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
        while True:
            try:
                designation = input("Saisir le nom du produit : ").strip()
                if designation.replace(" ", "").isalpha():
                    break
                print("Le nom doit contenir uniquement des lettres")
            except ValueError:
                print("Veuillez entrer uniquement des lettres")

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


# Menu principal
while True:
    print("\n=== Menu Boutique-Pro & Historique ===")
    print("1. Ajouter une catégorie")
    print("2. Lister les catégories")
    print("3. Ajouter un produit")
    print("4. Lister les produits")
    print("5. Ajouter ou Retirer stock")
    print("6. Produits avec stock < 5")
    print("0. Quitter")
    
    choix = input("Saisir votre choix : ")

    if choix == "1":
        ajouter_categorie()
    elif choix == "2":
        afficher_categorie()
    elif choix == "3":
        ajouter_produit()
    elif choix == "4":
        lister_produits()
    elif choix == "5":
        ajouter_mouvement()
    elif choix == "6":
        alerte_stock()
    elif choix == "0":
        print("Au revoir !")
        break
    else:
        print("Choix invalide")

# Fermeture de la connexion
curseur.close()
connexion.close()
