from graphs.graph_runner import MentalHealthGraphRunner
from config.settings import load_config
import sys

def main():
    """Main application entry point."""
    
    try:
        # Load configuration
        load_config()
        
        # Initialize graph runner
        runner = MentalHealthGraphRunner()
        
        print("🌟 Welcome to the Mental Health Support System")
        print("=" * 50)
        print("This is a safe space for mental health support and resources.")
        print("Type 'exit' or 'quit' to end the session at any time.")
        print("In case of emergency, please call 911 or go to your nearest emergency room.")
        print("=" * 50)
        
        # Start session
        session_id = runner.start_session()
        print(f"Session started. ID: {session_id[:8]}...")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'end']:
                    result = runner.end_session(session_id)
                    print(f"\nAssistant: {result['response']}")
                    break
                
                # Process message
                result = runner.process_message(session_id, user_input)
                
                # Display response
                print(f"\nAssistant ({result.get('current_agent', 'system')}): {result['response']}")
                
                # Show crisis level if elevated
                if result.get('crisis_level') and result['crisis_level'] >= 6:
                    print(f"\n⚠️  Crisis support activated (Level: {result['crisis_level']}/10)")
                
                # Check if session ended
                if not result.get('session_active', True):
                    break
                
                print()
                
            except KeyboardInterrupt:
                print("\n\nSession interrupted. Ending safely...")
                result = runner.end_session(session_id)
                print(f"Assistant: {result['response']}")
                break
            
            except Exception as e:
                print(f"\nError: {e}")
                print("Please try again or type 'exit' to end the session.")
                continue
    
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
