# Boutique-Pro_Historique

## Contexte
Cette application gère le stock d’une structure solidaire (type Simplon) avec un historique des mouvements.  
Elle permet de connaître le stock actuel, d’éviter les pertes ou vols, et de gérer les catégories et produits.

## Fonctionnalités

1. **Gestion des catégories**
   - Ajouter une catégorie
   - Lister les catégories existantes

2. **Catalogue produits**
   - Ajouter un produit associé à une catégorie
   - Lister tous les produits avec le nom de leur catégorie

3. **Mouvements de stock**
   - Ajouter ou retirer une quantité pour un produit
   - Historisation automatique des mouvements (Date, Produit, Quantité, Type : Entrée/Sortie)

4. **Alerte stock faible**
   - Afficher tous les produits dont le stock est inférieur à 5 unités

## Structure de la base de données

### Tables

1. **categories**
   - `id` (PK)
   - `nom_categorie` (varchar)

2. **produits**
   - `id` (PK)
   - `designation` (varchar)
   - `prix` (decimal)
   - `stock` (int)
   - `categorie_id` (FK vers categories.id)

3. **mouvements**
   - `id` (PK)
   - `id_produit` (FK vers produits.id)
   - `quantite` (int)
   - `type_mouvement` (ENTREE / SORTIE)
   - `date_mouvement` (datetime)

## Dépendances

- Python 
- MySQL  
- Module Python : mysql-connector-python

## Installation

1. Cloner le dépôt GitHub  
2. Créer la base de données boutique_pro_historique et les tables categories, produits, mouvements  
3. Installer la dépendance :  
   pip install mysql-connector-python

## Authentification des utilisateurs 
L’application possède un système d’authentification avec protection des mots de passe.
## Inscription
Lors de la création d’un compte :
l’email est contrôlé pour vérifier que le format est valide ;
l’adresse est vérifiée pour éviter les doublons dans la base ;
le rôle accepté est admin ou user ;
le mot de passe n’est jamais enregistré en clair.
Avant l’insertion dans la base de données, le mot de passe est transformé en une empreinte numérique grâce au module hashlib.
La base conserve uniquement cette valeur chiffrée.
## Connexion
Au moment de l’identification :
l’utilisateur saisit son email et son mot de passe ;
le système applique le même algorithme de hachage sur le mot de passe saisi ;
le résultat est comparé avec la valeur stockée.
Si les deux correspondent, l’accès est autorisé et la session démarre.
Gestion des droits
Une fois connecté, les options du menu varient selon le rôle :
admin : opérations de gestion (ajout catégorie, produits, stock) ;
user : consultation.

## Déconnexion
Il est possible de fermer la session à tout moment pour revenir au menu d’accueil.
Sécurité apportée
Même en cas d’accès à la base, les mots de passe réels ne sont pas visibles, car seule leur empreinte est conservée.

## Note important
### Configuration du port MySQL

Le port utilisé dans le code est `3307` car c’est celui configuré sur ma machine.
Selon votre installation, MySQL utilise souvent `3306`.
Si la connexion échoue, modifiez simplement la valeur du port dans le fichier Python pour mettre celui de votre environnement.

