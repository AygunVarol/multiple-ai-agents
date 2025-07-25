"""
Statistical analysis and visualization of experimental results
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
import pandas as pd

class ResultsAnalyzer:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.plots_dir = self.output_dir / 'plots'
        self.plots_dir.mkdir(parents=True, exist_ok=True)
        
        # Set plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def analyze_all_scenarios(self, results):
        """Analyze results from all scenarios"""
        print("Generating comprehensive analysis...")
        
        # Generate comparison plots
        self._plot_response_time_comparison(results)
        self._plot_cpu_utilization_analysis(results)
        self._plot_accuracy_comparison(results)
        self._plot_throughput_analysis(results)
        self._plot_failover_analysis(results)
        self._plot_load_balancing_effectiveness(results)
        
        # Generate statistical summary
        stats_summary = self._generate_statistical_summary(results)
        self._save_summary_report(stats_summary)
        
        print(f"Analysis complete. Plots saved to {self.plots_dir}/")
        return stats_summary
    
    def _plot_response_time_comparison(self, results):
        """Plot response time comparison across scenarios"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Response Time Analysis Across Scenarios', fontsize=16)
        
        # S1: Normal Operation Response Times
        if 'S1' in results:
            s1_data = self._extract_response_times(results['S1'])
            if s1_data:
                axes[0, 0].hist(s1_data, bins=30, alpha=0.7, color='skyblue')
                axes[0, 0].set_title('S1: Normal Operation Response Times')
                axes[0, 0].set_xlabel('Response Time (ms)')
                axes[0, 0].set_ylabel('Frequency')
                axes[0, 0].axvline(np.mean(s1_data), color='red', linestyle='--', 
                                  label=f'Mean: {np.mean(s1_data):.1f}ms')
                axes[0, 0].legend()
        
        # S2: Failover Response Times (Before vs After)
        if 'S2' in results:
            s2_before = self._extract_failover_response_times(results['S2'], 'before')
            s2_after = self._extract_failover_response_times(results['S2'], 'after')
            
            if s2_before and s2_after:
                axes[0, 1].hist(s2_before, bins=20, alpha=0.7, label='Before Failure', color='lightgreen')
                axes[0, 1].hist(s2_after, bins=20, alpha=0.7, label='After Recovery', color='lightcoral')
                axes[0, 1].set_title('S2: Failover Response Times')
                axes[0, 1].set_xlabel('Response Time (ms)')
                axes[0, 1].set_ylabel('Frequency')
                axes[0, 1].legend()
        
        # S3: Load Balancing (Supervisor vs RPi)
        if 'S3' in results:
            s3_supervisor, s3_rpi = self._extract_load_balancing_response_times(results['S3'])
            
            if s3_supervisor and s3_rpi:
                axes[1, 0].hist(s3_supervisor, bins=20, alpha=0.7, label='Supervisor', color='gold')
                axes[1, 0].hist(s3_rpi, bins=20, alpha=0.7, label='RPi', color='mediumpurple')
                axes[1, 0].set_title('S3: Load Balancing Response Times')
                axes[1, 0].set_xlabel('Response Time (ms)')
                axes[1, 0].set_ylabel('Frequency')
                axes[1, 0].legend()
        
        # Overall comparison boxplot
        all_scenario_data = []
        labels = []
        
        for scenario_id in ['S1', 'S2', 'S3']:
            if scenario_id in results:
                if scenario_id == 'S1':
                    data = self._extract_response_times(results[scenario_id])
                    if data:
                        all_scenario_data.append(data)
                        labels.append('S1: Normal')
                elif scenario_id == 'S2':
                    before_data = self._extract_failover_response_times(results[scenario_id], 'before')
                    after_data = self._extract_failover_response_times(results[scenario_id], 'after')
                    if before_data:
                        all_scenario_data.append(before_data)
                        labels.append('S2: Before')
                    if after_data:
                        all_scenario_data.append(after_data)
                        labels.append('S2: After')
                elif scenario_id == 'S3':
                    sup_data, rpi_data = self._extract_load_balancing_response_times(results[scenario_id])
                    if sup_data:
                        all_scenario_data.append(sup_data)
                        labels.append('S3: Supervisor')
                    if rpi_data:
                        all_scenario_data.append(rpi_data)
                        labels.append('S3: RPi')
        
        if all_scenario_data:
            axes[1, 1].boxplot(all_scenario_data, labels=labels)
            axes[1, 1].set_title('Response Time Comparison')
            axes[1, 1].set_ylabel('Response Time (ms)')
            axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(self.plots_dir / 'response_time_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_cpu_utilization_analysis(self, results):
        """Plot CPU utilization analysis"""
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('CPU Utilization Analysis', fontsize=16)
        
        for idx, (scenario_id, scenario_data) in enumerate(results.items()):
            if idx >= 3:  # Only plot first 3 scenarios
                break
                
            cpu_data = self._extract_cpu_usage(scenario_data)
            if cpu_data:
                time_points = list(range(len(cpu_data)))
                axes[idx].plot(time_points, cpu_data, alpha=0.7, linewidth=2)
                axes[idx].set_title(f'{scenario_id}: CPU Usage Over Time')
                axes[idx].set_xlabel('Time Points')
                axes[idx].set_ylabel('CPU Usage (%)')
                axes[idx].axhline(y=70, color='red', linestyle='--', alpha=0.8, 
                                 label='Load Threshold (70%)')
                axes[idx].grid(True, alpha=0.3)
                axes[idx].legend()
                
                # Add statistics
                mean_cpu = np.mean(cpu_data)
                max_cpu = np.max(cpu_data)
                axes[idx].text(0.02, 0.98, f'Mean: {mean_cpu:.1f}%\nMax: {max_cpu:.1f}%', 
                              transform=axes[idx].transAxes, verticalalignment='top',
                              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig(self.plots_dir / 'cpu_utilization_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_accuracy_comparison(self, results):
        """Plot accuracy comparison across scenarios"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Accuracy Analysis Across Scenarios', fontsize=16)
        
        # Accuracy distribution
        accuracy_data = []
        labels = []
        
        for scenario_id, scenario_data in results.items():
            acc_scores = self._extract_accuracy_scores(scenario_data)
            if acc_scores:
                accuracy_data.append(acc_scores)
                labels.append(scenario_id)
        
        if accuracy_data:
            axes[0].boxplot(accuracy_data, labels=labels)
            axes[0].set_title('Accuracy Distribution by Scenario')
            axes[0].set_ylabel('Accuracy Score (%)')
            axes[0].grid(True, alpha=0.3)
        
        # Accuracy vs Response Time scatter
        for scenario_id, scenario_data in results.items():
            acc_scores = self._extract_accuracy_scores(scenario_data)
            resp_times = self._extract_response_times(scenario_data)
            
            if acc_scores and resp_times and len(acc_scores) == len(resp_times):
                axes[1].scatter(resp_times, acc_scores, alpha=0.6, label=scenario_id, s=30)
        
        axes[1].set_title('Accuracy vs Response Time')
        axes[1].set_xlabel('Response Time (ms)')
        axes[1].set_ylabel('Accuracy Score (%)')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.plots_dir / 'accuracy_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_throughput_analysis(self, results):
        """Plot throughput analysis"""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        throughput_data = []
        scenario_names = []
        
        for scenario_id, scenario_data in results.items():
            throughput = self._calculate_throughput(scenario_data)
            throughput_data.append(throughput)
            scenario_names.append(scenario_id)
        
        if throughput_data:
            bars = ax.bar(scenario_names, throughput_data, color=['skyblue', 'lightcoral', 'lightgreen'])
            ax.set_title('Task Throughput by Scenario', fontsize=14)
            ax.set_ylabel('Tasks per Minute')
            ax.set_xlabel('Scenario')
            
            # Add value labels on bars
            for bar, value in zip(bars, throughput_data):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{value:.1f}', ha='center', va='bottom')
            
            ax.grid(True, alpha=0.3, axis='y')
        
        plt.savefig(self.plots_dir / 'throughput_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_failover_analysis(self, results):
        """Plot detailed failover analysis for S2"""
        if 'S2' not in results:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Scenario 2: Failover Analysis Details', fontsize=16)
        
        s2_data = results['S2']
        
        # Failover timeline
        failover_metrics = self._extract_failover_metrics(s2_data)
        if failover_metrics:
            timeline_labels = ['Detection Time', 'Election Time', 'Total Downtime']
            timeline_values = [
                failover_metrics.get('avg_detection_time', 0),
                failover_metrics.get('avg_election_time', 0),
                failover_metrics.get('avg_downtime', 0)
            ]
            
            axes[0, 0].bar(timeline_labels, timeline_values, color=['orange', 'red', 'darkred'])
            axes[0, 0].set_title('Average Failover Timeline')
            axes[0, 0].set_ylabel('Time (seconds)')
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # Add value labels
            for i, v in enumerate(timeline_values):
                axes[0, 0].text(i, v + 0.1, f'{v:.2f}s', ha='center', va='bottom')
        
        # Performance degradation
        performance_degradation = [
            run.get('performance_degradation', 0) for run in s2_data
        ]
        if performance_degradation:
            axes[0, 1].hist(performance_degradation, bins=10, alpha=0.7, color='coral')
            axes[0, 1].set_title('Performance Degradation Distribution')
            axes[0, 1].set_xlabel('Performance Degradation (%)')
            axes[0, 1].set_ylabel('Frequency')
            axes[0, 1].axvline(np.mean(performance_degradation), color='red', 
                              linestyle='--', label=f'Mean: {np.mean(performance_degradation):.1f}%')
            axes[0, 1].legend()
        
        # Recovery success rate
        recovery_rates = [
            run.get('recovery_success_rate', 0) for run in s2_data
        ]
        if recovery_rates:
            axes[1, 0].boxplot(recovery_rates)
            axes[1, 0].set_title('Recovery Success Rate')
            axes[1, 0].set_ylabel('Success Rate')
            axes[1, 0].set_xticklabels(['S2'])
        
        # Tasks before vs after failure
        tasks_before = [run.get('tasks_before_failure', 0) for run in s2_data]
        tasks_after = [run.get('tasks_after_recovery', 0) for run in s2_data]
        
        if tasks_before and tasks_after:
            x = np.arange(len(tasks_before))
            width = 0.35
            
            axes[1, 1].bar(x - width/2, tasks_before, width, label='Before Failure', alpha=0.8)
            axes[1, 1].bar(x + width/2, tasks_after, width, label='After Recovery', alpha=0.8)
            axes[1, 1].set_title('Task Completion: Before vs After Failure')
            axes[1, 1].set_ylabel('Number of Tasks')
            axes[1, 1].set_xlabel('Experiment Run')
            axes[1, 1].legend()
        
        plt.tight_layout()
        plt.savefig(self.plots_dir / 'failover_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_load_balancing_effectiveness(self, results):
        """Plot load balancing effectiveness for S3"""
        if 'S3' not in results:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Scenario 3: Load Balancing Analysis', fontsize=16)
        
        s3_data = results['S3']
        
        # Load distribution
        supervisor_tasks = [run.get('tasks_on_supervisor', 0) for run in s3_data]
        rpi_tasks = [run.get('tasks_on_rpis', 0) for run in s3_data]
        
        if supervisor_tasks and rpi_tasks:
            total_tasks = [s + r for s, r in zip(supervisor_tasks, rpi_tasks)]
            supervisor_ratio = [s/t if t > 0 else 0 for s, t in zip(supervisor_tasks, total_tasks)]
            rpi_ratio = [r/t if t > 0 else 0 for r, t in zip(rpi_tasks, total_tasks)]
            
            x = np.arange(len(supervisor_tasks))
            width = 0.6
            
            axes[0, 0].bar(x, supervisor_ratio, width, label='Supervisor', alpha=0.8)
            axes[0, 0].bar(x, rpi_ratio, width, bottom=supervisor_ratio, label='RPis', alpha=0.8)
            axes[0, 0].set_title('Task Distribution Ratio')
            axes[0, 0].set_ylabel('Proportion of Tasks')
            axes[0, 0].set_xlabel('Experiment Run')
            axes[0, 0].legend()
        
        # Load shedding events
        load_shedding_events = [run.get('load_shedding_events', 0) for run in s3_data]
        if load_shedding_events:
            axes[0, 1].plot(load_shedding_events, marker='o', linewidth=2, markersize=6)
            axes[0, 1].set_title('Load Shedding Events per Run')
            axes[0, 1].set_ylabel('Number of Events')
            axes[0, 1].set_xlabel('Experiment Run')
            axes[0, 1].grid(True, alpha=0.3)
        
        # Response time comparison (Supervisor vs RPi)
        avg_resp_supervisor = [run.get('avg_response_supervisor', 0) for run in s3_data]
        avg_resp_rpi = [run.get('avg_response_rpi', 0) for run in s3_data]
        
        if avg_resp_supervisor and avg_resp_rpi:
            comparison_data = [
                [rt for rt in avg_resp_supervisor if rt > 0],
                [rt for rt in avg_resp_rpi if rt > 0]
            ]
            
            if all(comparison_data):
                axes[1, 0].boxplot(comparison_data, labels=['Supervisor', 'RPi'])
                axes[1, 0].set_title('Response Time Comparison')
                axes[1, 0].set_ylabel('Average Response Time (ms)')
        
        # Load balancing effectiveness scores
        effectiveness_scores = [
            run.get('load_balancing_effectiveness', 0) for run in s3_data
        ]
        if effectiveness_scores:
            axes[1, 1].bar(range(len(effectiveness_scores)), effectiveness_scores, 
                          color='lightgreen', alpha=0.8)
            axes[1, 1].set_title('Load Balancing Effectiveness Score')
            axes[1, 1].set_ylabel('Effectiveness Score (0-100)')
            axes[1, 1].set_xlabel('Experiment Run')
            axes[1, 1].axhline(y=80, color='red', linestyle='--', alpha=0.8, 
                              label='Target (80%)')
            axes[1, 1].legend()
        
        plt.tight_layout()
        plt.savefig(self.plots_dir / 'load_balancing_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _generate_statistical_summary(self, results):
        """Generate comprehensive statistical summary"""
        summary = {
            'experiment_overview': {
                'total_scenarios': len(results),
                'scenarios_analyzed': list(results.keys()),
                'analysis_timestamp': pd.Timestamp.now().isoformat()
            },
            'scenario_summaries': {}
        }
        
        for scenario_id, scenario_data in results.items():
            scenario_summary = {
                'iterations': len(scenario_data),
                'performance_metrics': self._calculate_scenario_performance(scenario_data),
                'statistical_tests': self._perform_statistical_tests(scenario_data)
            }
            summary['scenario_summaries'][scenario_id] = scenario_summary
        
        # Cross-scenario comparisons
        summary['cross_scenario_analysis'] = self._perform_cross_scenario_analysis(results)
        
        return summary
    
    def _calculate_scenario_performance(self, scenario_data):
        """Calculate performance metrics for a scenario"""
        response_times = self._extract_response_times(scenario_data)
        accuracy_scores = self._extract_accuracy_scores(scenario_data)
        cpu_usage = self._extract_cpu_usage(scenario_data)
        
        metrics = {}
        
        if response_times:
            metrics['response_time'] = {
                'mean': np.mean(response_times),
                'median': np.median(response_times),
                'std': np.std(response_times),
                'min': np.min(response_times),
                'max': np.max(response_times),
                'p95': np.percentile(response_times, 95),
                'p99': np.percentile(response_times, 99)
            }
        
        if accuracy_scores:
            metrics['accuracy'] = {
                'mean': np.mean(accuracy_scores),
                'median': np.median(accuracy_scores),
                'std': np.std(accuracy_scores),
                'min': np.min(accuracy_scores),
                'max': np.max(accuracy_scores)
            }
        
        if cpu_usage:
            metrics['cpu_utilization'] = {
                'mean': np.mean(cpu_usage),
                'median': np.median(cpu_usage),
                'std': np.std(cpu_usage),
                'max': np.max(cpu_usage),
                'time_above_threshold': np.sum(np.array(cpu_usage) > 70) / len(cpu_usage)
            }
        
        return metrics
    
    def _perform_statistical_tests(self, scenario_data):
        """Perform statistical tests on scenario data"""
        response_times = self._extract_response_times(scenario_data)
        
        tests = {}
        
        if len(response_times) > 30:  # Sufficient sample size
            # Normality test
            _, p_value_normality = stats.shapiro(response_times)
            tests['normality_test'] = {
                'test': 'Shapiro-Wilk',
                'p_value': p_value_normality,
                'is_normal': p_value_normality > 0.05
            }
            
            # Confidence interval for mean response time
            confidence_interval = stats.t.interval(
                0.95, len(response_times)-1,
                loc=np.mean(response_times),
                scale=stats.sem(response_times)
            )
            tests['confidence_interval_95'] = {
                'lower': confidence_interval[0],
                'upper': confidence_interval[1]
            }
        
        return tests
    
    def _perform_cross_scenario_analysis(self, results):
        """Perform statistical comparisons between scenarios"""
        analysis = {}
        
        # Compare response times between scenarios
        scenario_response_times = {}
        for scenario_id, scenario_data in results.items():
            response_times = self._extract_response_times(scenario_data)
            if response_times:
                scenario_response_times[scenario_id] = response_times
        
        # Pairwise t-tests
        if len(scenario_response_times) >= 2:
            scenario_pairs = []
            scenario_ids = list(scenario_response_times.keys())
            
            for i in range(len(scenario_ids)):
                for j in range(i+1, len(scenario_ids)):
                    s1, s2 = scenario_ids[i], scenario_ids[j]
                    data1, data2 = scenario_response_times[s1], scenario_response_times[s2]
                    
                    if len(data1) > 10 and len(data2) > 10:
                        # Perform t-test
                        t_stat, p_value = stats.ttest_ind(data1, data2)
                        
                        scenario_pairs.append({
                            'scenario_1': s1,
                            'scenario_2': s2,
                            't_statistic': t_stat,
                            'p_value': p_value,
                            'significant_difference': p_value < 0.05,
                            'mean_1': np.mean(data1),
                            'mean_2': np.mean(data2)
                        })
            
            analysis['pairwise_comparisons'] = scenario_pairs
        
        return analysis
    
    def _save_summary_report(self, summary):
        """Save comprehensive summary report"""
        # JSON summary
        with open(self.output_dir / 'statistical_summary.json', 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        # Human-readable report
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("MULTI-AGENT LLM SYSTEM EVALUATION REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Analysis Date: {summary['experiment_overview']['analysis_timestamp']}")
        report_lines.append(f"Scenarios Analyzed: {', '.join(summary['experiment_overview']['scenarios_analyzed'])}")
        report_lines.append("")
        
        # Scenario summaries
        for scenario_id, scenario_summary in summary['scenario_summaries'].items():
            report_lines.append(f"SCENARIO {scenario_id} SUMMARY")
            report_lines.append("-" * 30)
            report_lines.append(f"Iterations: {scenario_summary['iterations']}")
            
            if 'response_time' in scenario_summary['performance_metrics']:
                rt_metrics = scenario_summary['performance_metrics']['response_time']
                report_lines.append(f"Response Time - Mean: {rt_metrics['mean']:.2f}ms, "
                                  f"P95: {rt_metrics['p95']:.2f}ms, P99: {rt_metrics['p99']:.2f}ms")
            
            if 'accuracy' in scenario_summary['performance_metrics']:
                acc_metrics = scenario_summary['performance_metrics']['accuracy']
                report_lines.append(f"Accuracy - Mean: {acc_metrics['mean']:.2f}%, "
                                  f"Std: {acc_metrics['std']:.2f}%")
            
            if 'cpu_utilization' in scenario_summary['performance_metrics']:
                cpu_metrics = scenario_summary['performance_metrics']['cpu_utilization']
                report_lines.append(f"CPU Usage - Mean: {cpu_metrics['mean']:.1f}%, "
                                  f"Max: {cpu_metrics['max']:.1f}%, "
                                  f"Time Above 70%: {cpu_metrics['time_above_threshold']*100:.1f}%")
            
            report_lines.append("")
        
        # Cross-scenario analysis
        if 'cross_scenario_analysis' in summary and 'pairwise_comparisons' in summary['cross_scenario_analysis']:
            report_lines.append("CROSS-SCENARIO STATISTICAL COMPARISONS")
            report_lines.append("-" * 40)
            
            for comparison in summary['cross_scenario_analysis']['pairwise_comparisons']:
                significance = "SIGNIFICANT" if comparison['significant_difference'] else "Not significant"
                report_lines.append(f"{comparison['scenario_1']} vs {comparison['scenario_2']}: "
                                  f"p={comparison['p_value']:.4f} ({significance})")
                report_lines.append(f"  Mean response times: {comparison['mean_1']:.2f}ms vs "
                                  f"{comparison['mean_2']:.2f}ms")
            
            report_lines.append("")
        
        # Save report
        with open(self.output_dir / 'evaluation_report.txt', 'w') as f:
            f.write('\n'.join(report_lines))
    
    # Helper methods for data extraction
    def _extract_response_times(self, scenario_data):
        """Extract response times from scenario data"""
        response_times = []
        for run in scenario_data:
            if 'response_times' in run and run['response_times']:
                response_times.extend(run['response_times'])
        return response_times
    
    def _extract_failover_response_times(self, scenario_data, phase):
        """Extract response times from failover scenario"""
        response_times = []
        key = f'response_times_{phase}'
        for run in scenario_data:
            if key in run and run[key]:
                response_times.extend(run[key])
        return response_times
    
    def _extract_load_balancing_response_times(self, scenario_data):
        """Extract response times from load balancing scenario"""
        supervisor_times = []
        rpi_times = []
        for run in scenario_data:
            if 'response_times_supervisor' in run:
                supervisor_times.extend(run['response_times_supervisor'])
            if 'response_times_rpi' in run:
                rpi_times.extend(run['response_times_rpi'])
        return supervisor_times, rpi_times
    
    def _extract_accuracy_scores(self, scenario_data):
        """Extract accuracy scores from scenario data"""
        accuracy_scores = []
        for run in scenario_data:
            if 'accuracy_scores' in run and run['accuracy_scores']:
                accuracy_scores.extend(run['accuracy_scores'])
        return accuracy_scores
    
    def _extract_cpu_usage(self, scenario_data):
        """Extract CPU usage data from scenario data"""
        cpu_usage = []
        for run in scenario_data:
            if 'cpu_usage' in run and run['cpu_usage']:
                cpu_usage.extend(run['cpu_usage'])
            elif 'cpu_usage_timeline' in run:
                cpu_timeline = [m.get('supervisor_cpu', 0) for m in run['cpu_usage_timeline']]
                cpu_usage.extend(cpu_timeline)
        return cpu_usage
    
    def _extract_failover_metrics(self, scenario_data):
        """Extract failover-specific metrics"""
        detection_times = []
        election_times = []
        downtimes = []
        
        for run in scenario_data:
            if 'failure_detection_time' in run:
                detection_times.append(run['failure_detection_time'])
            if 'leader_election_time' in run:
                election_times.append(run['leader_election_time'])
            if 'downtime' in run:
                downtimes.append(run['downtime'])
        
        if detection_times and election_times and downtimes:
            return {
                'avg_detection_time': np.mean(detection_times),
                'avg_election_time': np.mean(election_times),
                'avg_downtime': np.mean(downtimes)
            }
        return {}
    
    def _calculate_throughput(self, scenario_data):
        """Calculate throughput (tasks per minute)"""
        total_tasks = 0
        total_duration = 0
        
        for run in scenario_data:
            if 'tasks_completed' in run:
                total_tasks += run['tasks_completed']
            if 'total_duration' in run:
                total_duration += run['total_duration']
            elif 'phase_1_duration' in run and 'phase_2_duration' in run:
                total_duration += run['phase_1_duration'] + run['phase_2_duration']
        
        if total_duration > 0:
            return (total_tasks / total_duration) * 60  # tasks per minute
        return 0