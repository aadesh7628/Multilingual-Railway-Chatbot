import pandas as pd
from typing import Optional, List, Dict, Tuple
import google.generativeai as genai

class Bot:
    def __init__(self, api_token: str):
        self.api_token = api_token
        # Load CSV data
        self.df = pd.read_csv('chatRailways/chatbotModule/data/indianRailwaysData.csv')
        
        # Initialize Google's Gemini Pro model
        genai.configure(api_key=api_token)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Railway-related keywords for query classification
        self.railway_keywords = [
            "train", "platform", "ticket", "departure", "depart", "leave", "arrival", 
            "distance", "schedule", "railway", "station", "express",
            "rajdhani", "shatabdi", "duronto", "superfast", "mail",
            "irctc", "reservation", "booking", "cancel", "refund",
            "rail", "coach", "compartment", "berth", "seat"
        ]
        
        # Initialize chat history
        self.chat_history = []

    def is_railway_query(self, query: str) -> bool:
        """Check if the query is related to railways."""
        return any(keyword in query.lower() for keyword in self.railway_keywords)

    def extract_stations_from_query(self, query: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract source and destination stations from the query."""
        query = query.lower()
        stations = set(station.lower() for station in 
                      pd.concat([self.df['From Station'], self.df['To Station']])
                      if isinstance(station, str) and station.strip())
        
        from_station = None
        to_station = None
        
        for station in stations:
            if station in query:
                if f"from {station}" in query or f"at {station}" in query:
                    from_station = station
                elif f"to {station}" in query:
                    to_station = station
                elif not from_station:
                    from_station = station
                elif not to_station:
                    to_station = station

        return (from_station.title() if from_station else None,
                to_station.title() if to_station else None)

    def find_trains_between_stations(self, from_station: str, to_station: str) -> List[Dict]:
        """Find all trains running between two stations."""
        trains = self.df[
            (self.df['From Station'].str.lower() == from_station.lower()) &
            (self.df['To Station'].str.lower() == to_station.lower())
        ]
        return trains.to_dict('records')

    def format_train_list(self, trains: List[Dict]) -> str:
        """Format a list of trains in a readable format using HTML."""
        if not trains:
            return "No trains found for this route."

        response = '<div class="train-list">'
        response += '<h3>🚂 Trains Available:</h3>'

        for train in trains:
            response += f'''
                <div class="train-card">
                    <div class="train-header">
                        <strong>🚂 {train.get('Train Name', 'Unknown Train')}</strong>
                    </div>
                    <div class="train-details">
                        <p>🕒 <strong>Departure:</strong> {train.get('Departure Time', 'N/A')}</p>
                        <p>🕒 <strong>Arrival:</strong> {train.get('Arrival Time', 'N/A')}</p>
                        <p>🚉 <strong>Platform:</strong> {train.get('Platform', 'N/A')}</p>
                        <p>💰 <strong>Fare:</strong> ₹{train.get('Ticket Price (INR)', 'N/A')}</p>
                    </div>
                </div>
            '''
        response += '</div>'
        return response


    def format_train_info(self, train_info: Dict, query_type: str = None) -> str:
        """Format train information based on query type using HTML."""
        if query_type == 'arrival':
            return f"🚂 The {train_info.get('Train Name', 'Train')} arrives at {train_info.get('Arrival Time', 'N/A')}."
        
        elif query_type == 'departure':
            return f"🚂 The {train_info.get('Train Name', 'Train')} departs at {train_info.get('Departure Time', 'N/A')}."
        
        elif query_type == 'platform':
            return f"🚉 The {train_info.get('Train Name', 'Train')} arrives at {train_info.get('Platform', 'N/A')}."
        
        elif query_type == 'price':
            return f"💰 The ticket price for {train_info.get('Train Name', 'Train')} is ₹{train_info.get('Ticket Price (INR)', 'N/A')}."
        
        elif query_type == 'distance':
            return f"📏 The distance covered by {train_info.get('Train Name', 'Train')} is {train_info.get('Distance (km)', 'N/A')} km."
        
        # Default comprehensive response
        return f'''
            <div class="train-details-card">
                <div class="train-details-header">
                    <h3>Train Details</h3>
                </div>
                <div class="train-details-content">
                    <p>🚂 <strong>Train:</strong> {train_info.get('Train Name', 'Unknown')}</p>
                    <p>📍 <strong>From:</strong> {train_info.get('From Station', 'N/A')}</p>
                    <p>📍 <strong>To:</strong> {train_info.get('To Station', 'N/A')}</p>
                    <p>🕒 <strong>Departure:</strong> {train_info.get('Departure Time', 'N/A')}</p>
                    <p>🕒 <strong>Arrival:</strong> {train_info.get('Arrival Time', 'N/A')}</p>
                    <p>🚉 <strong>Platform:</strong> {train_info.get('Platform', 'N/A')}</p>
                    <p>📏 <strong>Distance:</strong> {train_info.get('Distance (km)', 'N/A')} km</p>
                    <p>💰 <strong>Fare:</strong> ₹{train_info.get('Ticket Price (INR)', 'N/A')}</p>
                </div>
            </div>
        '''
    
    def generate_general_response(self, query: str) -> str:
        """Generate response for general railway queries using Gemini Pro."""
        prompt = f"""
        As an Indian Railways expert, please provide a detailed and accurate response to this query:
        
        {query}
        
        Please ensure the response:
        1. Is specific to Indian Railways
        2. Includes relevant facts and procedures
        3. Mentions official sources when applicable
        4. Is comprehensive and well-structured
        
        If the query is not about Indian Railways, politely decline to answer.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return "I apologize, but I'm having trouble generating a response. Please try asking about specific train schedules, platforms, or ticket prices."

    def determine_query_type(self, query: str) -> str:
        """Determine the specific type of query."""
        query = query.lower()
        if "arrival" in query and "departure" not in query:
            return "arrival"
        elif "departure" in query and "arrival" not in query:
            return "departure"
        elif "departure" in query or "leave" in query:
            return "departure"
        elif "platform" in query:
            return "platform"
        elif "price" in query or "fare" in query or "cost" in query:
            return "price"
        elif "distance" in query:
            return "distance"
        return None

    def chat(self, user_query: str) -> str:
        """Process user query and return appropriate response."""
        if not user_query:
            return "Please provide a question."

        if not self.is_railway_query(user_query):
            return "I'm sorry, but I can only answer railway-related queries. Please ask me about Indian Railways, trains, schedules, platforms, or ticket prices."

        # Extract stations and determine query type
        from_station, to_station = self.extract_stations_from_query(user_query)
        query_type = self.determine_query_type(user_query)
        
        # Handle train listings between stations
        if from_station and to_station:
            trains = self.find_trains_between_stations(from_station, to_station)
            if trains:
                if len(trains) > 1:
                    return self.format_train_list(trains)
                else:
                    return self.format_train_info(trains[0], query_type)
        
        # Look for specific train information
        for _, train in self.df.iterrows():
            train_name = str(train['Train Name']).lower()
            if train_name in user_query.lower():
                return self.format_train_info(train.to_dict(), query_type)
        
        # Handle general railway queries
        if any(keyword in user_query.lower() for keyword in ["how", "what", "why", "when", "where", "can", "do", "is", "are"]):
            return self.generate_general_response(user_query)
        
        return "I couldn't find specific information about that in my database. Please check the train name or stations and try again."



# import pandas as pd
# from typing import Optional, List, Dict, Tuple
# import google.generativeai as genai
# from django.utils.safestring import mark_safe
# class Bot:
#     def __init__(self, api_token: str):
#         self.api_token = api_token
#         # Load CSV data
#         self.df = pd.read_csv('chatRailways/chatbotModule/data/indianRailwaysData.csv')
        
#         # Initialize Google's Gemini Pro model
#         genai.configure(api_key=api_token)
#         self.model = genai.GenerativeModel('gemini-pro')
        
#         # Railway-related keywords for query classification
#         self.railway_keywords = [
#             "train", "platform", "ticket", "departure", "arrival", 
#             "distance", "schedule", "railway", "station", "express",
#             "rajdhani", "shatabdi", "duronto", "superfast", "mail",
#             "irctc", "reservation", "booking", "cancel", "refund",
#             "rail", "coach", "compartment", "berth", "seat"
#         ]
        
#         # Initialize chat history
#         self.chat_history = []

#     def is_railway_query(self, query: str) -> bool:
#         """Check if the query is related to railways."""
#         return any(keyword in query.lower() for keyword in self.railway_keywords)

#     def extract_stations_from_query(self, query: str) -> Tuple[Optional[str], Optional[str]]:
#         """Extract source and destination stations from the query."""
#         query = query.lower()
#         stations = set(station.lower() for station in 
#                       pd.concat([self.df['From Station'], self.df['To Station']])
#                       if isinstance(station, str) and station.strip())
        
#         from_station = None
#         to_station = None
        
#         for station in stations:
#             if station in query:
#                 if f"from {station}" in query or f"at {station}" in query:
#                     from_station = station
#                 elif f"to {station}" in query:
#                     to_station = station
#                 elif not from_station:
#                     from_station = station
#                 elif not to_station:
#                     to_station = station

#         return (from_station.title() if from_station else None,
#                 to_station.title() if to_station else None)

#     def find_trains_between_stations(self, from_station: str, to_station: str) -> List[Dict]:
#         """Find all trains running between two stations."""
#         trains = self.df[
#             (self.df['From Station'].str.lower() == from_station.lower()) &
#             (self.df['To Station'].str.lower() == to_station.lower())
#         ]
#         return trains.to_dict('records')

#     def format_train_list(self, trains: List[Dict]) -> str:
#         """Format a list of trains in a readable format similar to the image."""
#         if not trains:
#             return "No trains found for this route."
            
#         response = "🚂 Trains Available:"
        
#         for train in trains:
#             response += f" ————————————— Train Details —————————————"
#             response += f" 🚂 {train['Train Name']}"
#             response += f" 🕒 Departure: {train['Departure Time']}"
#             response += f" 🕒 Arrival: {train['Arrival Time']}"
#             response += f" 🚉 Platform: Platform {train['Platform']}"
#             response += f" 💰 Fare: ₹{train['Ticket Price (INR)']}"
#             response += " ——————————————————————————————————————"
        
#         return response

#     def format_train_info(self, train_info: Dict, query_type: str = None) -> str:
#         """Format train information similar to the image format."""
#         if query_type == 'arrival':
#             return f"🚂 The {train_info['Train Name']} arrives at {train_info['Arrival Time']}."
            
#         elif query_type == 'departure':
#             return f"🚂 The {train_info['Train Name']} departs at {train_info['Departure Time']}."
            
#         elif query_type == 'platform':
#             return f"🚉 The {train_info['Train Name']} arrives at Platform {train_info['Platform']}."
            
#         elif query_type == 'price':
#             return f"💰 The ticket price for {train_info['Train Name']} is ₹{train_info['Ticket Price (INR)']}."
            
#         elif query_type == 'distance':
#             return f"📏 The distance covered by {train_info['Train Name']} is {train_info['Distance (km)']} km."
            
#         # Default comprehensive response
#         response = " —————————————————— Train Details —————————————————"
#         response += f" 🚂 {train_info['Train Name']} "
#         response += f" 📍 From: {train_info['From Station']}"
#         response += f" 📍 To: {train_info['To Station']}"
#         response += f" 🕒 Departure: {train_info['Departure Time']}"
#         response += f" 🕒 Arrival: {train_info['Arrival Time']}"
#         response += f" 🚉 Platform: Platform {train_info['Platform']}"
#         response += f" 📏 Distance: {train_info['Distance (km)']} km"
#         response += f" 💰 Fare: ₹{train_info['Ticket Price (INR)']}"
#         response += " ——————————————————————————————————————"
#         return response


#     def generate_general_response(self, query: str) -> str:
#         """Generate response for general railway queries using Gemini Pro."""
#         prompt = f"""
#         As an Indian Railways expert, please provide a detailed and accurate response to this query:
        
#         {query}
        
#         Please ensure the response:
#         1. Is specific to Indian Railways
#         2. Includes relevant facts and procedures
#         3. Mentions official sources when applicable
#         4. Is comprehensive and well-structured
        
#         If the query is not about Indian Railways, politely decline to answer.
#         """
        
#         try:
#             response = self.model.generate_content(prompt)
#             return response.text
#         except Exception as e:
#             return "I apologize, but I'm having trouble generating a response. Please try asking about specific train schedules, platforms, or ticket prices."

#     def determine_query_type(self, query: str) -> str:
#         """Determine the specific type of query."""
#         query = query.lower()
#         if "arrival" in query and "departure" not in query:
#             return "arrival"
#         elif "departure" in query and "arrival" not in query:
#             return "departure"
#         elif "platform" in query:
#             return "platform"
#         elif "price" in query or "fare" in query or "cost" in query:
#             return "price"
#         elif "distance" in query:
#             return "distance"
#         return None

#     def chat(self, user_query: str) -> str:
#         """Process user query and return appropriate response."""
#         if not user_query:
#             return "Please provide a question."

#         if not self.is_railway_query(user_query):
#             return "I'm sorry, but I can only answer railway-related queries. Please ask me about Indian Railways, trains, schedules, platforms, or ticket prices."

#         # Extract stations and determine query type
#         from_station, to_station = self.extract_stations_from_query(user_query)
#         query_type = self.determine_query_type(user_query)
        
#         # Handle train listings between stations
#         if from_station and to_station:
#             trains = self.find_trains_between_stations(from_station, to_station)
#             if trains:
#                 if len(trains) > 1:
#                     return self.format_train_list(trains)
#                 else:
#                     return self.format_train_info(trains[0], query_type)
        
#         # Look for specific train information
#         for _, train in self.df.iterrows():
#             train_name = str(train['Train Name']).lower()
#             if train_name in user_query.lower():
#                 return self.format_train_info(train.to_dict(), query_type)
        
#         # Handle general railway queries
#         if any(keyword in user_query.lower() for keyword in ["how", "what", "why", "when", "where", "can", "do", "is", "are"]):
#             return self.generate_general_response(user_query)
        
#         return "I couldn't find specific information about that in my database. Please check the train name or stations and try again."





# import requests
# import time
# import pandas as pd
# from typing import Optional, List, Dict

# class HuggingFaceLLM:
#     def __init__(self, api_token: str):
#         self.api_token = api_token

#     def generate_response(self, prompt: str) -> str:
#         api_url = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-125M"
#         headers = {"Authorization": f"Bearer {self.api_token}"}
#         payload = {
#             "inputs": prompt,
#             "parameters": {
#                 "max_length": 300,
#                 "return_full_text": False,
#                 "temperature": 0.7,  # Adjust creativity level
#                 "top_p": 0.9        # Use top-p sampling for diversity
#             }
#         }


#         max_retries = 5
#         retry_delay = 10

#         for attempt in range(max_retries):
#             response = requests.post(api_url, headers=headers, json=payload)
#             if response.status_code == 200:
#                 output = response.json()
#                 print("Raw Response:", output)  # Log the raw output
#                 if output and isinstance(output, list) and "generated_text" in output[0]:
#                     return output[0]["generated_text"]
#                 else:
#                     print("Unexpected response format:", output)
#                     return "Unexpected response format from API."
#             elif response.status_code == 503 and "currently loading" in response.text:
#                 print(f"Model is loading. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
#                 time.sleep(retry_delay)
#             else:
#                 print("Error:", response.status_code, response.text)
#                 return f"Error: {response.status_code}, {response.text}"

#         return "The model could not generate a response after multiple attempts."



# class Bot:
#     def __init__(self, api_token: str):
#         self.api_token = api_token
#         self.df = pd.read_csv('chatRailways/chatbotModule/data/indianRailwaysData.csv')
#         # Fill NaN values with empty strings for string columns
#         string_columns = ['Train Name', 'From Station', 'To Station', 'Arrival Time', 
#                          'Departure Time', 'Platform']
#         self.df[string_columns] = self.df[string_columns].fillna('')
#         self.chat_history = []

#     def find_trains_between_stations(self, from_station: str, to_station: str) -> List[Dict]:
#         """Find all trains running between two stations."""
#         trains = self.df[
#             (self.df['From Station'].str.lower() == from_station.lower()) &
#             (self.df['To Station'].str.lower() == to_station.lower())
#         ]
#         return trains.to_dict('records')

#     def extract_stations_from_query(self, query: str) -> tuple[Optional[str], Optional[str]]:
#         """Extract source and destination stations from the query."""
#         query = query.lower()
#         # Convert stations to sets after removing empty strings and converting to lowercase
#         stations = set(station.lower() for station in 
#                       pd.concat([self.df['From Station'], self.df['To Station']])
#                       if isinstance(station, str) and station.strip())
        
#         from_station = None
#         to_station = None
        
#         # Look for stations in the query
#         for station in stations:
#             if station in query:
#                 # Check if it's mentioned with "from" or "to"
#                 if f"from {station}" in query or f"at {station}" in query:
#                     from_station = station
#                 elif f"to {station}" in query:
#                     to_station = station
#                 # If no preposition is used, try to determine order
#                 elif not from_station:
#                     from_station = station
#                 elif not to_station:
#                     to_station = station

#         # Capitalize station names to match the original data
#         if from_station:
#             from_station = from_station.title()
#         if to_station:
#             to_station = to_station.title()

#         return from_station, to_station

#     def find_train_info(self, query: str) -> Optional[dict]:
#         """Search for train information based on the query parameters."""
#         query = query.lower()
        
#         # First try to find by train name
#         for _, train in self.df.iterrows():
#             train_name = str(train['Train Name']).lower()
#             if train_name in query:
#                 return train.to_dict()

#         # If no train name found, try to find by stations
#         from_station, to_station = self.extract_stations_from_query(query)
#         if from_station and to_station:
#             trains = self.find_trains_between_stations(from_station, to_station)
#             if trains:
#                 return trains[0]

#         return None

#     def format_response(self, query: str, train_info: dict) -> str:
#         """Format the response based on the query type and train information."""
#         query = query.lower()
        
#         if "platform" in query:
#             return f"The {train_info['Train Name']} arrives at {train_info['Platform']}."
        
#         elif "price" in query or "ticket" in query:
#             return f"The ticket price for {train_info['Train Name']} from {train_info['From Station']} to {train_info['To Station']} is ₹{train_info['Ticket Price (INR)']}."
        
#         elif "time" in query or "arrive" in query or "depart" in query:
#             return f"The {train_info['Train Name']} arrives at {train_info['Arrival Time']} and departs at {train_info['Departure Time']}."
        
#         elif "distance" in query:
#             return f"The distance between {train_info['From Station']} and {train_info['To Station']} covered by {train_info['Train Name']} is {train_info['Distance (km)']} km."
        
#         # For queries about trains between stations
#         elif any(word in query for word in ["which train", "what train", "trains between", "available train"]):
#             from_station, to_station = self.extract_stations_from_query(query)
#             if from_station and to_station:
#                 trains = self.find_trains_between_stations(from_station, to_station)
#                 if trains:
#                     response = f"The following trains are available from {from_station} to {to_station}:\n\n" + f"\n\n"
#                     for train in trains:
#                         response += f"- {train['Train Name']}\n"
#                         response += f"  Departure: {train['Departure Time']}\n"
#                         response += f"  Arrival: {train['Arrival Time']}\n"
#                         response += f"  Platform: {train['Platform']}\n"
#                         response += f"  Ticket Price: ₹{train['Ticket Price (INR)']}\n\n"
#                     return response.strip()
            
#         # Default response with all information
#         return f"Train: {train_info['Train Name']}\nFrom: {train_info['From Station']}\nTo: {train_info['To Station']}\nArrival: {train_info['Arrival Time']}\nDeparture: {train_info['Departure Time']}\nPlatform: {train_info['Platform']}\nDistance: {train_info['Distance (km)']} km\nTicket Price: ₹{train_info['Ticket Price (INR)']}"

#     def is_railway_query(self, query: str) -> bool:
#         """Check if the query is related to railways."""
#         railway_keywords = [
#             "train", "platform", "ticket", "departure", "arrival", 
#             "distance", "schedule", "railway", "station", "express",
#             "rajdhani", "shatabdi", "duronto", "superfast", "mail"
#         ]
#         return any(keyword in query.lower() for keyword in railway_keywords)

#     def chat(self, user_query: str) -> str:
#         """Process user query and return appropriate response."""
#         if not user_query:
#             return "Please provide a question."

#         if not self.is_railway_query(user_query):
#             response = "I'm sorry, but I can only answer railway-related queries. Please ask me about trains, schedules, platforms, or ticket prices."
#             self.chat_history.append((user_query, response))
#             return response

#         train_info = self.find_train_info(user_query)

#         if train_info:
#             response = self.format_response(user_query, train_info)

#         else:
#             if any(keyword in user_query.lower() for keyword in ["how", "what", "why", "when", "where"]):
#                 enhanced_prompt = f"""
#                 Answer the query by considering yourself as a Expert Indian Railway chatbot. I will give a query about the Indian Railway System or Issues about indian trains or indian train bookings or ticket cancellations. So for these type of queries please find the answer and retrun it, if you don't know about it then simple say so and if query asks you to provide large informations then return the website link or source link
                 
#                 User Query: "{user_query}"
#                 """

#                 hf_llm = HuggingFaceLLM(self.api_token)
#                 response = hf_llm.generate_response(enhanced_prompt)
#                 # print("LLM Response:", response)
#                 response = response.strip()
#                 if not response or response.isspace():
#                     response = "I'm sorry, I couldn't find an answer to your query. Please try again later."
#             else:
#                 response = "I couldn't find specific information about that in my database. Could you please check the train name or stations and try again?"
            
#         self.chat_history.append((user_query, response))
#         return response