import pandas as pd
import requests
import datetime

def background_agent():
    print(f"Agent activated at {datetime.datetime.now()}")
    
    # Free, open source live data feed for globally registered startup lists
    url = "https://raw.githubusercontent.com/MainakRepositor/Datasets/master/Indian%20startups%20funding%20in%202021.csv"
    
    try:
        df_raw = pd.read_csv(url)
        
        # Build out structural column frames
        df_cleaned = pd.DataFrame()
        df_cleaned['Date Tracked'] = datetime.date.today().strftime("%Y-%m-%d")
        df_cleaned['Startup Name'] = df_raw['Company/Brand'].fillna('Unknown')
        df_cleaned['CEO / Founders'] = df_raw['Founder/s'].fillna('Not Listed')
        df_cleaned['Sector'] = df_raw['Sector'].fillna('Tech')
        df_cleaned['Headquarters'] = df_raw['Headquarters'].fillna('India')
        
        # Formulate standard predicted business emails
        def predict_email(row):
            founder = str(row['CEO / Founders']).split(',')[0].strip().lower().split(' ')[0]
            domain = str(row['Startup Name']).replace(' ', '').lower().replace('.','')
            if founder and founder != 'not':
                return f"{founder}@{domain}.com"
            return "info@company.com"
            
        df_cleaned['Predicted Email'] = df_cleaned.apply(predict_email, axis=1)
        df_cleaned = df_cleaned.drop_duplicates(subset=['Startup Name'])
        
        # Save it into the repo folder
        df_cleaned.to_csv("latest_ceo_leads.csv", index=False)
        print(f"Agent compiled {len(df_cleaned)} rows into the dataset successfully.")
        
    except Exception as e:
        print(f"Agent encountered a pipeline error: {e}")

if __name__ == "__main__":
    background_agent()
