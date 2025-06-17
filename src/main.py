import argparse
import sys
from .santa_assigner import SantaAssigner
from .exceptions import SecretSantaError


def parse_arguments():
    parser = argparse.ArgumentParser(description='Secret Santa Assignment System')
    parser.add_argument('--input', required=True,
                      help='Path to input CSV file with employee information')
    parser.add_argument('--previous', required=False,
                      help='Path to CSV file with previous year\'s assignments')
    parser.add_argument('--output', required=True,
                      help='Path where to save the output CSV file')
    return parser.parse_args()


def main():
    try:
        args = parse_arguments()
        
        # Initialize the Secret Santa assigner
        assigner = SantaAssigner()
        
        # Load employee data
        assigner.load_employees(args.input)
        
        # Load previous assignments if provided
        if args.previous:
            assigner.load_previous_assignments(args.previous)
        
        # Generate new assignments
        assignments = assigner.generate_assignments()
        
        # Save the assignments
        assigner.save_assignments(assignments, args.output)
        
        print(f"Successfully generated Secret Santa assignments and saved to {args.output}")
        return 0
        
    except SecretSantaError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())