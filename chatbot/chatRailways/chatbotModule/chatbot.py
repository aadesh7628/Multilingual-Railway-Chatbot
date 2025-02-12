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