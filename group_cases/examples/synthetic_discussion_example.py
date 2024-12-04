"""
Example of using synthetic data generation for discussions.
"""
from group_cases.src.utils.synthetic_data import SyntheticDataGenerator
from group_cases.src.core.base_discussion import DiscussionType
import json
import os

def main():
    # Create generator with fixed seed for reproducibility
    generator = SyntheticDataGenerator(seed=42)
    
    # Generate data for different discussion types
    discussion_configs = [
        {
            "type": DiscussionType.BRAINSTORMING,
            "name": "product_features",
            "participants": 5,
            "steps": 4
        },
        {
            "type": DiscussionType.EVALUATION,
            "name": "design_review",
            "participants": 4,
            "steps": 3
        },
        {
            "type": DiscussionType.INTERVIEW,
            "name": "user_research",
            "participants": 3,
            "steps": 4
        }
    ]
    
    # Create output directory if it doesn't exist
    output_dir = "data/synthetic"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate and save data for each configuration
    for config in discussion_configs:
        # Generate discussion data
        data = generator.generate_discussion_data(
            discussion_type=config["type"],
            num_participants=config["participants"],
            num_steps=config["steps"]
        )
        
        # Save to file
        output_file = os.path.join(
            output_dir,
            f"{config['name']}_discussion.json"
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        print(f"Generated synthetic data for {config['name']}")
        print(f"Saved to: {output_file}")
        print(f"Participants: {config['participants']}")
        print(f"Steps: {config['steps']}")
        print("Summary metrics:")
        print(json.dumps(data['summary']['average_metrics'], indent=2))
        print("\n")

if __name__ == "__main__":
    main()
