from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

def Variabile_Migliore(dataframe: pd.DataFrame, variabile_impostata: str):
    try:
        # Data cleaning
        dataframe = dataframe.drop_duplicates()
        
        # Encoding categorical variables
        dataframe = pd.get_dummies(dataframe)
        
        # Feature and target separation
        X = dataframe.drop(columns=[variabile_impostata])
        y = dataframe[variabile_impostata]
        
        # Split the data into training and testing sets
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.25, random_state=1729)
        
        # Train the decision tree classifier
        clf = DecisionTreeClassifier(max_depth=4, random_state=1729)
        clf.fit(X_train, y_train)
        
        # Extract and display feature importance
        features_names = X_train.columns
        features_importance = pd.DataFrame(clf.feature_importances_, index=features_names, columns=['Importance']).sort_values(by='Importance', ascending=False)
        
        # Display the top 25 features
        print('Top 25 Features:')
        print(features_importance.head(25))
        
        return features_importance.head(25)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
Variabile_Migliore(ML_model, 'default')