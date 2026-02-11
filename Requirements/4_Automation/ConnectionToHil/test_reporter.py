"""
Test Reporter - Generates HTML reports for HIL tests

Creates detailed, visual HTML reports with:
- Test execution timeline
- Signal values (expected vs actual)
- Pass/Fail status with color coding
- Timestamps for each step
- Summary statistics
"""

from datetime import datetime
from pathlib import Path
import json


class TestReporter:
    """Generates detailed HTML reports for test execution"""
    
    def __init__(self, test_name, description=""):
        self.test_name = test_name
        self.description = description
        self.start_time = datetime.now()
        self.steps = []
        self.checks = []
        self.current_step = None
        self.failed = False
        
    def add_step(self, step_name, description=""):
        """Add a new test step"""
        step = {
            "name": step_name,
            "description": description,
            "timestamp": datetime.now(),
            "checks": [],
            "sets": []
        }
        self.steps.append(step)
        self.current_step = step
        return step
    
    def add_set(self, signal_name, value):
        """Record a signal set operation"""
        if self.current_step:
            self.current_step["sets"].append({
                "signal": signal_name,
                "value": value,
                "timestamp": datetime.now()
            })
    
    def add_check(self, signal_name, expected, actual, passed, tolerance=None):
        """Record a signal check operation"""
        check = {
            "signal": signal_name,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "tolerance": tolerance,
            "timestamp": datetime.now()
        }
        
        if self.current_step:
            self.current_step["checks"].append(check)
        
        self.checks.append(check)
        
        if not passed:
            self.failed = True
    
    def add_note(self, note):
        """Add a note to current step"""
        if self.current_step:
            if "notes" not in self.current_step:
                self.current_step["notes"] = []
            self.current_step["notes"].append({
                "text": note,
                "timestamp": datetime.now()
            })
    
    def generate_html(self, output_path="test_report.html"):
        """Generate HTML report file"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        total_checks = len(self.checks)
        passed_checks = sum(1 for c in self.checks if c["passed"])
        failed_checks = total_checks - passed_checks
        
        status = "FAILED" if self.failed else "PASSED"
        status_color = "#dc3545" if self.failed else "#28a745"
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Report - {self.test_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
        }}
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        
        .header p {{
            opacity: 0.9;
            font-size: 14px;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }}
        
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        .summary-card h3 {{
            font-size: 14px;
            color: #6c757d;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .summary-card .value {{
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }}
        
        .summary-card.status {{
            border-left-color: {status_color};
        }}
        
        .summary-card.status .value {{
            color: {status_color};
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .step {{
            margin-bottom: 30px;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .step-header {{
            background: #f8f9fa;
            padding: 15px 20px;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .step-header h3 {{
            color: #333;
            font-size: 18px;
        }}
        
        .step-time {{
            color: #6c757d;
            font-size: 13px;
        }}
        
        .step-body {{
            padding: 20px;
        }}
        
        .step-description {{
            color: #6c757d;
            margin-bottom: 15px;
            font-style: italic;
        }}
        
        .sets, .checks {{
            margin-top: 15px;
        }}
        
        .sets h4, .checks h4 {{
            font-size: 14px;
            color: #495057;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .set-item {{
            background: #e7f3ff;
            padding: 10px 15px;
            margin-bottom: 8px;
            border-radius: 4px;
            border-left: 3px solid #0066cc;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }}
        
        .set-item .signal {{
            font-weight: bold;
            color: #0066cc;
        }}
        
        .check-item {{
            padding: 12px 15px;
            margin-bottom: 8px;
            border-radius: 4px;
            border-left: 3px solid;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr auto;
            gap: 15px;
            align-items: center;
            font-size: 13px;
        }}
        
        .check-item.passed {{
            background: #d4edda;
            border-left-color: #28a745;
        }}
        
        .check-item.failed {{
            background: #f8d7da;
            border-left-color: #dc3545;
        }}
        
        .check-signal {{
            font-weight: bold;
            font-family: 'Courier New', monospace;
        }}
        
        .check-expected, .check-actual {{
            font-family: 'Courier New', monospace;
        }}
        
        .check-status {{
            text-align: right;
            font-weight: bold;
        }}
        
        .check-item.passed .check-status {{
            color: #28a745;
        }}
        
        .check-item.failed .check-status {{
            color: #dc3545;
        }}
        
        .notes {{
            margin-top: 15px;
            padding: 15px;
            background: #fff3cd;
            border-left: 3px solid #ffc107;
            border-radius: 4px;
        }}
        
        .notes h4 {{
            font-size: 14px;
            color: #856404;
            margin-bottom: 8px;
        }}
        
        .note-item {{
            color: #856404;
            font-size: 13px;
            margin-bottom: 5px;
        }}
        
        .footer {{
            padding: 20px 30px;
            background: #f8f9fa;
            border-top: 1px solid #dee2e6;
            text-align: center;
            color: #6c757d;
            font-size: 13px;
        }}
        
        @media print {{
            body {{
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{self.test_name}</h1>
            <p>{self.description}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card status">
                <h3>Status</h3>
                <div class="value">{status}</div>
            </div>
            
            <div class="summary-card">
                <h3>Duration</h3>
                <div class="value">{duration:.2f}s</div>
            </div>
            
            <div class="summary-card">
                <h3>Total Checks</h3>
                <div class="value">{total_checks}</div>
            </div>
            
            <div class="summary-card">
                <h3>Passed</h3>
                <div class="value" style="color: #28a745;">{passed_checks}</div>
            </div>
            
            <div class="summary-card">
                <h3>Failed</h3>
                <div class="value" style="color: #dc3545;">{failed_checks}</div>
            </div>
        </div>
        
        <div class="content">
            <h2 style="margin-bottom: 20px; color: #333;">Test Execution Details</h2>
"""
        
        # Add steps
        for step in self.steps:
            step_time = step["timestamp"].strftime("%H:%M:%S.%f")[:-3]
            
            html += f"""
            <div class="step">
                <div class="step-header">
                    <h3>{step["name"]}</h3>
                    <span class="step-time">{step_time}</span>
                </div>
                <div class="step-body">
"""
            
            if step["description"]:
                html += f"""
                    <p class="step-description">{step["description"]}</p>
"""
            
            # Add sets
            if step["sets"]:
                html += """
                    <div class="sets">
                        <h4>Signal Sets</h4>
"""
                for s in step["sets"]:
                    html += f"""
                        <div class="set-item">
                            <span class="signal">{s["signal"]}</span> = {s["value"]}
                        </div>
"""
                html += """
                    </div>
"""
            
            # Add checks
            if step["checks"]:
                html += """
                    <div class="checks">
                        <h4>Signal Checks</h4>
"""
                for c in step["checks"]:
                    status_class = "passed" if c["passed"] else "failed"
                    status_text = "✓ PASS" if c["passed"] else "✗ FAIL"
                    
                    tolerance_text = f" (±{c['tolerance']})" if c['tolerance'] else ""
                    
                    html += f"""
                        <div class="check-item {status_class}">
                            <div class="check-signal">{c["signal"]}</div>
                            <div class="check-expected">Expected: {c["expected"]}{tolerance_text}</div>
                            <div class="check-actual">Actual: {c["actual"]}</div>
                            <div class="check-status">{status_text}</div>
                        </div>
"""
                html += """
                    </div>
"""
            
            # Add notes
            if "notes" in step:
                html += """
                    <div class="notes">
                        <h4>Notes</h4>
"""
                for note in step["notes"]:
                    html += f"""
                        <div class="note-item">• {note["text"]}</div>
"""
                html += """
                    </div>
"""
            
            html += """
                </div>
            </div>
"""
        
        html += f"""
        </div>
        
        <div class="footer">
            Generated on {end_time.strftime("%Y-%m-%d %H:%M:%S")} | 
            Test started at {self.start_time.strftime("%Y-%m-%d %H:%M:%S")} | 
            Duration: {duration:.2f}s
        </div>
    </div>
</body>
</html>
"""
        
        # Write to file
        output_file = Path(output_path)
        output_file.write_text(html, encoding='utf-8')
        
        return str(output_file.absolute())
