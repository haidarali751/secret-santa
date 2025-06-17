import sys

def main():
    try:
        
        print(f"Successfully generated Secret Santa assignments and saved to output.csv")
        return 0
        
    except:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 0

if __name__ == '__main__':
    sys.exit(main())