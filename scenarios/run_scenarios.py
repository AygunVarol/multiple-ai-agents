#!/usr/bin/env python3
"""
Main scenario orchestrator for IEEE IoT Magazine paper experiments
"""

import argparse
import json
import time
import logging
from datetime import datetime
from pathlib import Path

from scenario_1_normal import NormalOperationScenario
from scenario_2_failover import FailoverScenario  
from scenario_3_loadbalance import LoadBalancingScenario
from metrics_collector import MetricsCollector
from results_analyzer import ResultsAnalyzer

class ScenarioOrchestrator:
    def __init__(self, output_dir="results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.output_dir / 'experiment.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.metrics = MetricsCollector(self.output_dir)
        self.scenarios = {
            'S1': NormalOperationScenario(self.metrics),
            'S2': FailoverScenario(self.metrics),
            'S3': LoadBalancingScenario(self.metrics)
        }
        
    def run_all_scenarios(self, iterations=10, duration_per_scenario=300):
        """Run all scenarios with specified iterations and duration"""
        results = {}
        
        self.logger.info(f"Starting experiment run with {iterations} iterations")
        self.logger.info(f"Duration per scenario: {duration_per_scenario} seconds")
        
        for scenario_id, scenario in self.scenarios.items():
            self.logger.info(f"Running Scenario {scenario_id}")
            scenario_results = []
            
            for i in range(iterations):
                self.logger.info(f"Iteration {i+1}/{iterations} for {scenario_id}")
                
                # Run scenario
                start_time = time.time()
                result = scenario.run(duration=duration_per_scenario)
                end_time = time.time()
                
                result['iteration'] = i + 1
                result['total_duration'] = end_time - start_time
                result['timestamp'] = datetime.now().isoformat()
                
                scenario_results.append(result)
                
                # Brief cooldown between iterations
                time.sleep(30)
            
            results[scenario_id] = scenario_results
            
            # Save intermediate results
            self._save_results(results, f"intermediate_{scenario_id}.json")
            
        # Final save and analysis
        self._save_results(results, "final_results.json")
        self._generate_analysis(results)
        
        return results
    
    def run_single_scenario(self, scenario_id, iterations=5, duration=300):
        """Run a single scenario"""
        if scenario_id not in self.scenarios:
            raise ValueError(f"Unknown scenario: {scenario_id}")
            
        scenario = self.scenarios[scenario_id]
        results = []
        
        for i in range(iterations):
            self.logger.info(f"Running {scenario_id} - Iteration {i+1}/{iterations}")
            result = scenario.run(duration=duration)
            result['iteration'] = i + 1
            result['timestamp'] = datetime.now().isoformat()
            results.append(result)
            
        self._save_results({scenario_id: results}, f"{scenario_id}_results.json")
        return results
    
    def _save_results(self, results, filename):
        """Save results to JSON file"""
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        self.logger.info(f"Results saved to {filepath}")
    
    def _generate_analysis(self, results):
        """Generate statistical analysis and plots"""
        analyzer = ResultsAnalyzer(self.output_dir)
        analyzer.analyze_all_scenarios(results)

def main():
    parser = argparse.ArgumentParser(description='Run IoT multi-agent scenarios')
    parser.add_argument('--scenario', choices=['S1', 'S2', 'S3', 'all'], 
                       default='all', help='Scenario to run')
    parser.add_argument('--iterations', type=int, default=10, 
                       help='Number of iterations per scenario')
    parser.add_argument('--duration', type=int, default=300, 
                       help='Duration per scenario run (seconds)')
    parser.add_argument('--output', default='results', 
                       help='Output directory')
    
    args = parser.parse_args()
    
    orchestrator = ScenarioOrchestrator(args.output)
    
    if args.scenario == 'all':
        results = orchestrator.run_all_scenarios(args.iterations, args.duration)
    else:
        results = orchestrator.run_single_scenario(args.scenario, args.iterations, args.duration)
    
    print(f"Experiment completed. Results saved to {args.output}/")

if __name__ == "__main__":
    main()