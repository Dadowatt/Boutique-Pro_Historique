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
