import sys
from agent import OrchestratorAgent
from colorama import init, Fore, Style

# Initialize colorama
init()

def main():
    print(f"{Fore.CYAN}Initializing Orchestrator Agent...{Style.RESET_ALL}")
    
    try:
        agent = OrchestratorAgent()
    except ValueError as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please update your .env file with your OPENROUTER_API_KEY.{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}Agent ready! (Multi-Agent Version Loaded){Style.RESET_ALL}")
    print(f"{Fore.GREEN}(Type 'quit' to exit){Style.RESET_ALL}")

    while True:
        try:
            user_input = input(f"\n{Fore.BLUE}You: {Style.RESET_ALL}")
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            
            if not user_input.strip():
                continue

            response = agent.run(user_input)
            
            print(f"\n{Fore.MAGENTA}Agent:{Style.RESET_ALL}")
            print(response)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
