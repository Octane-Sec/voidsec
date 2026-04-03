import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Frame, Label
import threading
import time
import random
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class VoidEcosystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Void Ecosystem v1.1 - AI-Augmented Cyber Range")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0a14')
        
        # Set application icon (using a placeholder)
        try:
            self.root.iconbitmap("void_icon.ico")  # You would need to create this file
        except:
            pass
        
        # State variables
        self.is_running = False
        self.lab_status = "Offline"
        self.ai_status = "Standby"
        self.network_status = "Disconnected"
        self.active_labs = 0
        self.current_lab = None
        self.licensing_mode = "Non-Commercial (FOSS)"
        
        # Initialize metrics
        self.inference_speed = 0
        self.cpu_usage = 0
        self.memory_usage = 0
        self.latency = 0
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.create_widgets()
        
        # Start the metrics update thread
        self.update_metrics()
        
    def configure_styles(self):
        # Configure custom styles
        self.style.configure('Title.TLabel', 
                            background='#0a0a14', 
                            foreground='#00ffff', 
                            font=('Consolas', 18, 'bold'))
        
        self.style.configure('Subtitle.TLabel', 
                            background='#0a0a14', 
                            foreground='#00ffaa', 
                            font=('Consolas', 12, 'bold'))
        
        self.style.configure('Status.TLabel', 
                            background='#0a0a14', 
                            foreground='#ffffff', 
                            font=('Consolas', 10))
        
        self.style.configure('StatusValue.TLabel', 
                            background='#0a0a14', 
                            foreground='#00ff00', 
                            font=('Consolas', 10, 'bold'))
        
        self.style.configure('Warning.TLabel', 
                            background='#0a0a14', 
                            foreground='#ff6600', 
                            font=('Consolas', 10, 'bold'))
        
        self.style.configure('Button.TButton', 
                            background='#123456', 
                            foreground='#ffffff',
                            font=('Consolas', 10))
        
        self.style.map('Button.TButton',
                      background=[('active', '#1c5c8f')])
        
        self.style.configure('Frame.TFrame', 
                            background='#151522', 
                            relief='raised', 
                            borderwidth=1)
        
        self.style.configure('Console.TFrame', 
                            background='#000000', 
                            relief='sunken', 
                            borderwidth=1)
        
        self.style.configure('Header.TFrame', 
                            background='#070710')
        
        self.style.configure('Notebook.TNotebook', 
                            background='#0a0a14', 
                            borderwidth=0)
        
        self.style.configure('Notebook.TNotebook.Tab', 
                            background='#151522', 
                            foreground='#cccccc',
                            padding=[10, 5],
                            font=('Consolas', 10))
        
        self.style.map('Notebook.TNotebook.Tab',
                      background=[('selected', '#1a1a2e')],
                      foreground=[('selected', '#00ffff')])
    
    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self.root, style='Header.TFrame')
        header_frame.pack(fill='x', padx=10, pady=10)
        
        # Logo and title
        logo_frame = ttk.Frame(header_frame, style='Header.TFrame')
        logo_frame.pack(fill='x', pady=5)
        
        # Placeholder for logo - in a real app, you would load an image here
        logo_label = ttk.Label(logo_frame, text="VOID", style='Title.TLabel')
        logo_label.pack(side='left', padx=10)
        
        title_label = ttk.Label(logo_frame, 
                               text="AI-Augmented Cyber Range", 
                               style='Subtitle.TLabel')
        title_label.pack(side='left', padx=10, pady=5)
        
        # Licensing mode
        self.license_label = ttk.Label(logo_frame, 
                                      text=f"Mode: {self.licensing_mode}", 
                                      style='Status.TLabel')
        self.license_label.pack(side='right', padx=10)
        
        # Status bar
        status_frame = ttk.Frame(self.root, style='Frame.TFrame')
        status_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(status_frame, text="System Status:", style='Status.TLabel').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.system_status_label = ttk.Label(status_frame, text="Initializing...", style='StatusValue.TLabel')
        self.system_status_label.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(status_frame, text="AI Engine:", style='Status.TLabel').grid(row=0, column=2, padx=20, pady=5, sticky='w')
        self.ai_status_label = ttk.Label(status_frame, text=self.ai_status, style='StatusValue.TLabel')
        self.ai_status_label.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        
        ttk.Label(status_frame, text="Lab Status:", style='Status.TLabel').grid(row=0, column=4, padx=20, pady=5, sticky='w')
        self.lab_status_label = ttk.Label(status_frame, text=self.lab_status, style='StatusValue.TLabel')
        self.lab_status_label.grid(row=0, column=5, padx=5, pady=5, sticky='w')
        
        ttk.Label(status_frame, text="Network:", style='Status.TLabel').grid(row=0, column=6, padx=20, pady=5, sticky='w')
        self.network_status_label = ttk.Label(status_frame, text=self.network_status, style='StatusValue.TLabel')
        self.network_status_label.grid(row=0, column=7, padx=5, pady=5, sticky='w')
        
        # Control buttons
        button_frame = ttk.Frame(self.root, style='Frame.TFrame')
        button_frame.pack(fill='x', padx=10, pady=5)
        
        self.start_btn = ttk.Button(button_frame, text="Initialize System", command=self.toggle_system, style='Button.TButton')
        self.start_btn.pack(side='left', padx=5, pady=5)
        
        ttk.Button(button_frame, text="Deploy Lab", command=self.deploy_lab, style='Button.TButton').pack(side='left', padx=5, pady=5)
        ttk.Button(button_frame, text="Run Inference", command=self.run_inference, style='Button.TButton').pack(side='left', padx=5, pady=5)
        ttk.Button(button_frame, text="Security Audit", command=self.run_audit, style='Button.TButton').pack(side='left', padx=5, pady=5)
        ttk.Button(button_frame, text="Documentation", command=self.show_docs, style='Button.TButton').pack(side='left', padx=5, pady=5)
        ttk.Button(button_frame, text="Component Diagram", command=self.show_component_diagram, style='Button.TButton').pack(side='left', padx=5, pady=5)
        
        # Main content area with tabs
        notebook = ttk.Notebook(self.root, style='Notebook.TNotebook')
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Dashboard tab
        dashboard_frame = ttk.Frame(notebook, style='Frame.TFrame')
        notebook.add(dashboard_frame, text="Dashboard")
        self.create_dashboard_tab(dashboard_frame)
        
        # AI Inference tab
        ai_frame = ttk.Frame(notebook, style='Frame.TFrame')
        notebook.add(ai_frame, text="AI Inference")
        self.create_ai_tab(ai_frame)
        
        # Lab Management tab
        lab_frame = ttk.Frame(notebook, style='Frame.TFrame')
        notebook.add(lab_frame, text="Lab Management")
        self.create_lab_tab(lab_frame)
        
        # Network tab
        network_frame = ttk.Frame(notebook, style='Frame.TFrame')
        notebook.add(network_frame, text="Network Fabric")
        self.create_network_tab(network_frame)
        
        # Telemetry tab
        telemetry_frame = ttk.Frame(notebook, style='Frame.TFrame')
        notebook.add(telemetry_frame, text="Telemetry & Analytics")
        self.create_telemetry_tab(telemetry_frame)
        
        # Console output
        console_frame = ttk.Frame(self.root, style='Console.TFrame')
        console_frame.pack(fill='x', padx=10, pady=10)
        
        self.console = scrolledtext.ScrolledText(console_frame, 
                                               height=8, 
                                               bg='#000000', 
                                               fg='#00ff00', 
                                               font=('Consolas', 9),
                                               insertbackground='#00ff00')
        self.console.pack(fill='both', expand=True, padx=2, pady=2)
        self.console.insert('end', "System initialized. Ready to start Void Ecosystem...\n")
        self.console.configure(state='disabled')
    
    def create_dashboard_tab(self, parent):
        # Main dashboard with two columns
        main_frame = ttk.Frame(parent, style='Frame.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - System overview
        left_frame = ttk.Frame(main_frame, style='Frame.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(left_frame, text="SYSTEM OVERVIEW", style='Subtitle.TLabel').pack(pady=10)
        
        overview_text = """
Void Ecosystem Architecture:

- Intelligence Layer: Void (Proprietary)
- Control Plane: Void the Hack (Orchestrator)
- Inference Service: gRPC-based microservice
- Context Injection Gateway: Middleware for live state data
- Knowledge Base: Vector database with OST2/HTB docs

Performance Targets:
- Query Latency: < 250ms for standard queries
- Model: DeepSeek-Coder-V2 Lite (QLoRA)
- Parameters: 16B (compressed to ~8.5GB)
- Context Window: 32k tokens
- VRAM Allocation: 10GB dedicated to APU

Deployment Strategy:
- Single-Binary Installer (Java)
- Docker-based ecosystem
- Zero-Config experience
"""
        
        overview_label = ttk.Label(left_frame, text=overview_text, style='Status.TLabel', justify='left')
        overview_label.pack(pady=10, padx=10, anchor='w')
        
        # Right panel - Metrics and quick actions
        right_frame = ttk.Frame(main_frame, style='Frame.TFrame')
        right_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(right_frame, text="PERFORMANCE METRICS", style='Subtitle.TLabel').pack(pady=10)
        
        # Metrics display
        metrics_frame = ttk.Frame(right_frame, style='Frame.TFrame')
        metrics_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create a figure for metrics visualization
        fig = Figure(figsize=(5, 4), dpi=100, facecolor='#151522')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#151522')
        ax.tick_params(colors='white')
        
        # Sample data
        metrics = ['Inference Speed', 'CPU Usage', 'Memory Usage', 'Network Latency']
        values = [self.inference_speed, self.cpu_usage, self.memory_usage, self.latency]
        
        bars = ax.bar(metrics, values, color=['#00ffff', '#00ffaa', '#ffaa00', '#ff6600'])
        ax.set_ylabel('Value', color='white')
        ax.set_title('Current System Metrics', color='white')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                   f'{value}', ha='center', va='bottom', color='white')
        
        # Embed the plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, metrics_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Quick actions
        actions_frame = ttk.Frame(right_frame, style='Frame.TFrame')
        actions_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(actions_frame, text="QUICK ACTIONS", style='Subtitle.TLabel').pack(pady=5)
        
        action_buttons_frame = ttk.Frame(actions_frame, style='Frame.TFrame')
        action_buttons_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(action_buttons_frame, text="Quick Lab", command=self.quick_lab, style='Button.TButton').pack(side='left', padx=5)
        ttk.Button(action_buttons_frame, text="Run Diagnostics", command=self.run_diagnostics, style='Button.TButton').pack(side='left', padx=5)
        ttk.Button(action_buttons_frame, text="Check Updates", command=self.check_updates, style='Button.TButton').pack(side='left', padx=5)
    
    def create_ai_tab(self, parent):
        # AI inference controls
        main_frame = ttk.Frame(parent, style='Frame.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Settings panel
        settings_frame = ttk.Frame(main_frame, style='Frame.TFrame')
        settings_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(settings_frame, text="AI INFERENCE SETTINGS", style='Subtitle.TLabel').pack(pady=5)
        
        settings_grid = ttk.Frame(settings_frame, style='Frame.TFrame')
        settings_grid.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(settings_grid, text="Model:", style='Status.TLabel').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.model_var = tk.StringVar(value="DeepSeek-Coder-V2-Lite (4-bit Quantized)")
        model_combo = ttk.Combobox(settings_grid, textvariable=self.model_var, state="readonly", width=40)
        model_combo['values'] = ("DeepSeek-Coder-V2-Lite (4-bit Quantized)", "Void-Proprietary-Full", "Void-Lightweight")
        model_combo.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(settings_grid, text="Context Size:", style='Status.TLabel').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.context_var = tk.StringVar(value="32k tokens")
        context_combo = ttk.Combobox(settings_grid, textvariable=self.context_var, state="readonly", width=40)
        context_combo['values'] = ("16k tokens", "32k tokens", "64k tokens")
        context_combo.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(settings_grid, text="Hint Level:", style='Status.TLabel').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.hint_scale = ttk.Scale(settings_grid, from_=0, to=100, orient='horizontal')
        self.hint_scale.set(50)
        self.hint_scale.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        
        ttk.Label(settings_grid, text="Hint Level Value:", style='Status.TLabel').grid(row=2, column=2, sticky='w', padx=5, pady=5)
        self.hint_value_label = ttk.Label(settings_grid, text="50", style='StatusValue.TLabel')
        self.hint_value_label.grid(row=2, column=3, sticky='w', padx=5, pady=5)
        
        # Update hint value when scale changes
        self.hint_scale.configure(command=self.update_hint_value)
        
        # Query input
        query_frame = ttk.Frame(main_frame, style='Frame.TFrame')
        query_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(query_frame, text="QUERY INPUT", style='Subtitle.TLabel').pack(pady=5)
        
        self.query_text = scrolledtext.ScrolledText(query_frame, height=10, bg='#1a1a2e', fg='#ffffff', font=('Consolas', 10))
        self.query_text.pack(fill='both', expand=True, padx=10, pady=10)
        self.query_text.insert('end', "Describe the buffer overflow vulnerability in the current context...")
        
        button_frame = ttk.Frame(query_frame, style='Frame.TFrame')
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Submit Query", command=self.submit_query, style='Button.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_query, style='Button.TButton').pack(side='left', padx=5)
        
        # Response area
        response_frame = ttk.Frame(main_frame, style='Frame.TFrame')
        response_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(response_frame, text="AI RESPONSE", style='Subtitle.TLabel').pack(pady=5)
        
        self.response_text = scrolledtext.ScrolledText(response_frame, height=8, bg='#1a1a2e', fg='#00ffaa', font=('Consolas', 10))
        self.response_text.pack(fill='both', expand=True, padx=10, pady=10)
        self.response_text.insert('end', "AI responses will appear here...")
        self.response_text.configure(state='disabled')
    
    def create_lab_tab(self, parent):
        # Lab deployment controls
        main_frame = ttk.Frame(parent, style='Frame.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Lab configuration
        config_frame = ttk.Frame(main_frame, style='Frame.TFrame')
        config_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(config_frame, text="LAB CONFIGURATION", style='Subtitle.TLabel').pack(pady=5)
        
        config_grid = ttk.Frame(config_frame, style='Frame.TFrame')
        config_grid.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(config_grid, text="Lab Type:", style='Status.TLabel').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.lab_var = tk.StringVar(value="Buffer Overflow")
        lab_combo = ttk.Combobox(config_grid, textvariable=self.lab_var, state="readonly", width=30)
        lab_combo['values'] = ("Buffer Overflow", "ROP Chain", "Shellcode Development", "OSINT Investigation", "Web Application Testing")
        lab_combo.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(config_grid, text="Difficulty:", style='Status.TLabel').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.difficulty_var = tk.StringVar(value="Intermediate")
        difficulty_combo = ttk.Combobox(config_grid, textvariable=self.difficulty_var, state="readonly", width=30)
        difficulty_combo['values'] = ("Beginner", "Intermediate", "Advanced", "Expert")
        difficulty_combo.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(config_grid, text="Duration:", style='Status.TLabel').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.duration_var = tk.StringVar(value="60 minutes")
        duration_combo = ttk.Combobox(config_grid, textvariable=self.duration_var, state="readonly", width=30)
        duration_combo['values'] = ("30 minutes", "60 minutes", "120 minutes", "Unlimited")
        duration_combo.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(config_grid, text="Resources:", style='Status.TLabel').grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.resources_var = tk.StringVar(value="Standard (2CPU, 4GB RAM)")
        resources_combo = ttk.Combobox(config_grid, textvariable=self.resources_var, state="readonly", width=30)
        resources_combo['values'] = ("Light (1CPU, 2GB RAM)", "Standard (2CPU, 4GB RAM)", "Heavy (4CPU, 8GB RAM)")
        resources_combo.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        
        # Lab control buttons
        button_frame = ttk.Frame(config_frame, style='Frame.TFrame')
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Deploy Lab", command=self.deploy_lab, style='Button.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Snapshot Lab", command=self.snapshot_lab, style='Button.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Terminate Lab", command=self.terminate_lab, style='Button.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Reset Lab", command=self.reset_lab, style='Button.TButton').pack(side='left', padx=5)
        
        # Lab status and details
        status_frame = ttk.Frame(main_frame, style='Frame.TFrame')
        status_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(status_frame, text="ACTIVE LABS", style='Subtitle.TLabel').pack(pady=5)
        
        # Lab list
        columns = ("id", "type", "status", "duration", "resources")
        self.lab_tree = ttk.Treeview(status_frame, columns=columns, show='headings', height=8)
        self.lab_tree.heading("id", text="Lab ID")
        self.lab_tree.heading("type", text="Type")
        self.lab_tree.heading("status", text="Status")
        self.lab_tree.heading("duration", text="Duration")
        self.lab_tree.heading("resources", text="Resources")
        
        self.lab_tree.column("id", width=80)
        self.lab_tree.column("type", width=150)
        self.lab_tree.column("status", width=100)
        self.lab_tree.column("duration", width=100)
        self.lab_tree.column("resources", width=120)
        
        # Add scrollbar to treeview
        tree_scroll = ttk.Scrollbar(status_frame, orient="vertical", command=self.lab_tree.yview)
        self.lab_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.lab_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        tree_scroll.pack(side='right', fill='y', padx=(0, 10), pady=10)
        
        # Lab details
        details_frame = ttk.Frame(status_frame, style='Frame.TFrame')
        details_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(details_frame, text="LAB DETAILS", style='Subtitle.TLabel').pack(pady=5)
        
        self.lab_details = scrolledtext.ScrolledText(details_frame, height=10, bg='#1a1a2e', fg='#ffffff', font=('Consolas', 9))
        self.lab_details.pack(fill='both', expand=True, padx=10, pady=10)
        self.lab_details.insert('end', "Select a lab to view details...")
        self.lab_details.configure(state='disabled')
        
        # Bind selection event
        self.lab_tree.bind('<<TreeviewSelect>>', self.on_lab_select)
    
    def create_network_tab(self, parent):
        # Network visualization and controls
        main_frame = ttk.Frame(parent, style='Frame.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Network controls
        control_frame = ttk.Frame(main_frame, style='Frame.TFrame')
        control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(control_frame, text="NETWORK CONFIGURATION", style='Subtitle.TLabel').pack(pady=5)
        
        settings_frame = ttk.Frame(control_frame, style='Frame.TFrame')
        settings_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(settings_frame, text="Security Mesh:", style='Status.TLabel').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.mesh_var = tk.StringVar(value="WireGuard + Headscale")
        mesh_combo = ttk.Combobox(settings_frame, textvariable=self.mesh_var, state="readonly", width=30)
        mesh_combo['values'] = ("WireGuard + Headscale", "OpenVPN", "ZeroTier")
        mesh_combo.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(settings_frame, text="Isolation Level:", style='Status.TLabel').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.isolation_var = tk.StringVar(value="VPC per Student")
        isolation_combo = ttk.Combobox(settings_frame, textvariable=self.isolation_var, state="readonly", width=30)
        isolation_combo['values'] = ("VPC per Student", "Shared Network", "Full Isolation")
        isolation_combo.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(settings_frame, text="Encryption:", style='Status.TLabel').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.encryption_var = tk.StringVar(value="AES-256-GCM")
        encryption_combo = ttk.Combobox(settings_frame, textvariable=self.encryption_var, state="readonly", width=30)
        encryption_combo['values'] = ("AES-256-GCM", "ChaCha20-Poly1305", "AES-128-GCM")
        encryption_combo.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        # Network visualization
        viz_frame = ttk.Frame(main_frame, style='Frame.TFrame')
        viz_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(viz_frame, text="NETWORK TOPOLOGY", style='Subtitle.TLabel').pack(pady=5)
        
        canvas_frame = ttk.Frame(viz_frame, style='Frame.TFrame')
        canvas_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(canvas_frame, bg='#1a1a2e', highlightthickness=0)
        canvas.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Draw network diagram
        canvas.create_oval(50, 100, 100, 150, fill='#123456', outline='#00ffff', width=2)
        canvas.create_text(75, 125, text="AI\nEngine", fill='white', font=('Consolas', 8))
        
        canvas.create_oval(250, 50, 300, 100, fill='#561234', outline='#00ffaa', width=2)
        canvas.create_text(275, 75, text="Lab\nContainer", fill='white', font=('Consolas', 8))
        
        canvas.create_oval(250, 150, 300, 200, fill='#345612', outline='#00ffaa', width=2)
        canvas.create_text(275, 175, text="Lab\nContainer", fill='white', font=('Consolas', 8))
        
        canvas.create_oval(450, 100, 500, 150, fill='#125634', outline='#ffaa00', width=2)
        canvas.create_text(475, 125, text="Student\nNode", fill='white', font=('Consolas', 8))
        
        # Draw connections
        canvas.create_line(100, 125, 250, 75, fill='#00ff00', width=2, arrow=tk.LAST)
        canvas.create_line(100, 125, 250, 175, fill='#00ff00', width=2, arrow=tk.LAST)
        canvas.create_line(300, 75, 450, 125, fill='#00ff00', width=2, arrow=tk.LAST)
        canvas.create_line(300, 175, 450, 125, fill='#00ff00', width=2, arrow=tk.LAST)
        
        # Add labels
        canvas.create_text(300, 25, text="Software Defined Perimeter (SDP)", fill='#00ffff', font=('Consolas', 10, 'bold'))
        canvas.create_text(175, 60, text="gRPC", fill='#ffffff', font=('Consolas', 8))
        canvas.create_text(175, 190, text="gRPC", fill='#ffffff', font=('Consolas', 8))
        canvas.create_text(375, 90, text="WireGuard", fill='#ffffff', font=('Consolas', 8))
        canvas.create_text(375, 160, text="WireGuard", fill='#ffffff', font=('Consolas', 8))
        
        # Network status
        status_frame = ttk.Frame(main_frame, style='Frame.TFrame')
        status_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(status_frame, text="NETWORK STATUS", style='Subtitle.TLabel').pack(pady=5)
        
        status_grid = ttk.Frame(status_frame, style='Frame.TFrame')
        status_grid.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(status_grid, text="Connections:", style='Status.TLabel').grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.connections_label = ttk.Label(status_grid, text="0 active", style='StatusValue.TLabel')
        self.connections_label.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(status_grid, text="Data Transferred:", style='Status.TLabel').grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.data_label = ttk.Label(status_grid, text="0 MB", style='StatusValue.TLabel')
        self.data_label.grid(row=1, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(status_grid, text="Packet Loss:", style='Status.TLabel').grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.packet_loss_label = ttk.Label(status_grid, text="0%", style='StatusValue.TLabel')
        self.packet_loss_label.grid(row=2, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(status_grid, text="Security Status:", style='Status.TLabel').grid(row=0, column=2, sticky='w', padx=20, pady=2)
        self.security_status_label = ttk.Label(status_grid, text="Secure", style='StatusValue.TLabel')
        self.security_status_label.grid(row=0, column=3, sticky='w', padx=5, pady=2)
        
        ttk.Label(status_grid, text="Threats Detected:", style='Status.TLabel').grid(row=1, column=2, sticky='w', padx=20, pady=2)
        self.threats_label = ttk.Label(status_grid, text="0", style='StatusValue.TLabel')
        self.threats_label.grid(row=1, column=3, sticky='w', padx=5, pady=2)
    
    def create_telemetry_tab(self, parent):
        # Telemetry and analytics
        main_frame = ttk.Frame(parent, style='Frame.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Performance metrics
        perf_frame = ttk.Frame(main_frame, style='Frame.TFrame')
        perf_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(perf_frame, text="PERFORMANCE TELEMETRY", style='Subtitle.TLabel').pack(pady=5)
        
        # Create a figure with subplots
        fig = Figure(figsize=(10, 8), dpi=100, facecolor='#151522')
        fig.suptitle('System Performance Metrics', color='white')
        
        # CPU usage plot
        ax1 = fig.add_subplot(221)
        ax1.set_facecolor('#151522')
        ax1.tick_params(colors='white')
        ax1.set_title('CPU Usage (%)', color='white')
        self.cpu_data = [0] * 20
        self.cpu_line, = ax1.plot(self.cpu_data, color='#00ffaa')
        ax1.set_ylim(0, 100)
        
        # Memory usage plot
        ax2 = fig.add_subplot(222)
        ax2.set_facecolor('#151522')
        ax2.tick_params(colors='white')
        ax2.set_title('Memory Usage (GB)', color='white')
        self.memory_data = [0] * 20
        self.memory_line, = ax2.plot(self.memory_data, color='#ffaa00')
        ax2.set_ylim(0, 16)
        
        # Network latency plot
        ax3 = fig.add_subplot(223)
        ax3.set_facecolor('#151522')
        ax3.tick_params(colors='white')
        ax3.set_title('Network Latency (ms)', color='white')
        self.latency_data = [0] * 20
        self.latency_line, = ax3.plot(self.latency_data, color='#00ffff')
        ax3.set_ylim(0, 300)
        
        # Inference speed plot
        ax4 = fig.add_subplot(224)
        ax4.set_facecolor('#151522')
        ax4.tick_params(colors='white')
        ax4.set_title('Inference Speed (tokens/sec)', color='white')
        self.inference_data = [0] * 20
        self.inference_line, = ax4.plot(self.inference_data, color='#ff6600')
        ax4.set_ylim(0, 20)
        
        # Adjust layout
        fig.tight_layout()
        
        # Embed the plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, perf_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Student progress
        progress_frame = ttk.Frame(main_frame, style='Frame.TFrame')
        progress_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(progress_frame, text="STUDENT PROGRESS ANALYTICS", style='Subtitle.TLabel').pack(pady=5)
        
        progress_grid = ttk.Frame(progress_frame, style='Frame.TFrame')
        progress_grid.pack(fill='x', padx=10, pady=10)
        
        # Progress bars for different modules
        modules = ["Architecture 1001", "Buffer Overflow", "ROP Chains", "Shellcoding", "Web Exploitation"]
        self.progress_vars = {}
        
        for i, module in enumerate(modules):
            ttk.Label(progress_grid, text=module, style='Status.TLabel').grid(row=i, column=0, sticky='w', padx=5, pady=2)
            self.progress_vars[module] = tk.DoubleVar(value=random.randint(0, 100))
            progress_bar = ttk.Progressbar(progress_grid, variable=self.progress_vars[module], maximum=100)
            progress_bar.grid(row=i, column=1, sticky='ew', padx=5, pady=2)
            value_label = ttk.Label(progress_grid, text=f"{self.progress_vars[module].get():.1f}%", style='StatusValue.TLabel')
            value_label.grid(row=i, column=2, sticky='w', padx=5, pady=2)
        
        progress_grid.columnconfigure(1, weight=1)
    
    def update_hint_value(self, value):
        self.hint_value_label.config(text=f"{float(value):.0f}")
    
    def on_lab_select(self, event):
        selection = self.lab_tree.selection()
        if selection:
            item = self.lab_tree.item(selection[0])
            lab_id = item['values'][0]
            lab_type = item['values'][1]
            status = item['values'][2]
            duration = item['values'][3]
            resources = item['values'][4]
            
            self.lab_details.configure(state='normal')
            self.lab_details.delete(1.0, 'end')
            self.lab_details.insert('end', f"Lab ID: {lab_id}\n")
            self.lab_details.insert('end', f"Type: {lab_type}\n")
            self.lab_details.insert('end', f"Status: {status}\n")
            self.lab_details.insert('end', f"Duration: {duration}\n")
            self.lab_details.insert('end', f"Resources: {resources}\n\n")
            self.lab_details.insert('end', f"Details: This lab environment is configured for {lab_type} practice.\n")
            self.lab_details.insert('end', f"Current status is {status} with {duration} remaining.\n")
            self.lab_details.insert('end', f"Allocated resources: {resources}")
            self.lab_details.configure(state='disabled')
    
    def toggle_system(self):
        if not self.is_running:
            self.is_running = True
            self.start_btn.config(text="Shutdown System")
            self.system_status_label.config(text="Online")
            self.ai_status = "Initializing"
            self.ai_status_label.config(text=self.ai_status)
            self.lab_status = "Ready"
            self.lab_status_label.config(text=self.lab_status)
            self.network_status = "Establishing"
            self.network_status_label.config(text=self.network_status)
            
            self.console.configure(state='normal')
            self.console.insert('end', "Initializing Void Ecosystem...\n")
            self.console.insert('end', "Loading AI model (DeepSeek-Coder-V2-Lite)...\n")
            self.console.insert('end', "Establishing WireGuard mesh network...\n")
            self.console.insert('end', "System initialized successfully.\n")
            self.console.see('end')
            self.console.configure(state='disabled')
            
            # Simulate network connection establishment
            threading.Timer(2, self.complete_network_setup).start()
            
            # Simulate AI initialization
            threading.Timer(3, self.complete_ai_setup).start()
        else:
            self.is_running = False
            self.start_btn.config(text="Initialize System")
            self.system_status_label.config(text="Offline")
            self.ai_status = "Standby"
            self.ai_status_label.config(text=self.ai_status)
            self.lab_status = "Offline"
            self.lab_status_label.config(text=self.lab_status)
            self.network_status = "Disconnected"
            self.network_status_label.config(text=self.network_status)
            
            self.console.configure(state='normal')
            self.console.insert('end', "Shutting down Void Ecosystem...\n")
            self.console.insert('end', "All services terminated.\n")
            self.console.see('end')
            self.console.configure(state='disabled')
    
    def complete_network_setup(self):
        if self.is_running:
            self.network_status = "Connected"
            self.network_status_label.config(text=self.network_status)
            
            self.console.configure(state='normal')
            self.console.insert('end', "WireGuard mesh established. Zero-trust network active.\n")
            self.console.see('end')
            self.console.configure(state='disabled')
    
    def complete_ai_setup(self):
        if self.is_running:
            self.ai_status = "Ready"
            self.ai_status_label.config(text=self.ai_status)
            
            self.console.configure(state='normal')
            self.console.insert('end', "AI model loaded. Inference service available.\n")
            self.console.see('end')
            self.console.configure(state='disabled')
    
    def update_metrics(self):
        if self.is_running:
            # Simulate metric updates
            self.inference_speed = random.randint(8, 15)
            self.cpu_usage = random.randint(10, 80)
            self.memory_usage = random.randint(8, 14)
            self.latency = random.randint(20, 90)
            
            # Update telemetry data
            self.cpu_data = self.cpu_data[1:] + [self.cpu_usage]
            self.memory_data = self.memory_data[1:] + [self.memory_usage]
            self.latency_data = self.latency_data[1:] + [self.latency]
            self.inference_data = self.inference_data[1:] + [self.inference_speed]
            
            # Update plots if they exist
            if hasattr(self, 'cpu_line'):
                self.cpu_line.set_ydata(self.cpu_data)
                self.memory_line.set_ydata(self.memory_data)
                self.latency_line.set_ydata(self.latency_data)
                self.inference_line.set_ydata(self.inference_data)
                
                # Redraw the canvas
                self.root.after(100, self.redraw_plots)
            
            # Update network metrics
            self.connections_label.config(text=f"{random.randint(1, 5)} active")
            self.data_label.config(text=f"{random.randint(10, 100)} MB")
            self.packet_loss_label.config(text=f"{random.randint(0, 2)}%")
            
        # Schedule next update
        self.root.after(2000, self.update_metrics)
    
    def redraw_plots(self):
        if hasattr(self, 'canvas'):
            self.canvas.draw()
    
    def deploy_lab(self):
        if not self.is_running:
            messagebox.showwarning("System Offline", "Please initialize the system first.")
            return
        
        lab_type = self.lab_var.get()
        difficulty = self.difficulty_var.get()
        duration = self.duration_var.get()
        resources = self.resources_var.get()
        
        self.console.configure(state='normal')
        self.console.insert('end', f"Deploying {lab_type} lab ({difficulty})...\n")
        self.console.insert('end', f"Allocating {resources} for {duration}...\n")
        self.console.see('end')
        self.console.configure(state='disabled')
        
        # Add to lab tree
        lab_id = f"LAB-{random.randint(1000, 9999)}"
        self.lab_tree.insert("", "end", values=(lab_id, lab_type, "Deploying", duration, resources))
        self.active_labs += 1
        
        # Simulate lab deployment
        threading.Timer(2, lambda: self.lab_deployed(lab_id)).start()
    
    def lab_deployed(self, lab_id):
        if self.is_running:
            # Update the lab status in the treeview
            for item in self.lab_tree.get_children():
                if self.lab_tree.item(item)['values'][0] == lab_id:
                    values = list(self.lab_tree.item(item)['values'])
                    values[2] = "Active"
                    self.lab_tree.item(item, values=values)
                    break
            
            self.console.configure(state='normal')
            self.console.insert('end', f"Lab {lab_id} deployed successfully.\n")
            self.console.insert('end', "Secure tunnel established. Lab is now accessible.\n")
            self.console.see('end')
            self.console.configure(state='disabled')
    
    def run_inference(self):
        if not self.is_running:
            messagebox.showwarning("System Offline", "Please initialize the system first.")
            return
        
        query = self.query_text.get("1.0", "end-1c")
        if not query.strip():
            messagebox.showwarning("Empty Query", "Please enter a query for the AI.")
            return
        
        model = self.model_var.get()
        context_size = self.context_var.get()
        hint_level = self.hint_scale.get()
        
        self.console.configure(state='normal')
        self.console.insert('end', f"Processing query with {model} ({context_size})...\n")
        self.console.insert('end', f"Hint level set to {hint_level:.0f}%...\n")
        self.console.see('end')
        self.console.configure(state='disabled')
        
        # Simulate inference
        threading.Timer(1, self.inference_complete).start()
    
    def inference_complete(self):
        if self.is_running:
            responses = [
                "Based on the current CPU register state, the vulnerability appears to be a classic stack-based buffer overflow. The EIP register has been overwritten with 0x41414141, indicating successful control of execution flow.",
                "The assembly code shows improper bounds checking in the input handling function. The 'strcpy' function is being used without validating the length of the source buffer, making it susceptible to overflow.",
                "I recommend examining the return address overwrite possibility with a carefully crafted payload. The stack appears to be executable, so you could place shellcode in the buffer and redirect execution to it.",
                "The network traffic analysis indicates possible SQL injection points in the web application. The 'id' parameter in the GET request appears to be vulnerable based on the error messages returned."
            ]
            
            response = random.choice(responses)
            
            self.response_text.configure(state='normal')
            self.response_text.delete(1.0, 'end')
            self.response_text.insert('end', f"AI Response:\n\n{response}\n\n")
            self.response_text.insert('end', "Suggested next steps:\n")
            self.response_text.insert('end', "1. Examine the stack layout with 'info stack'\n")
            self.response_text.insert('end', "2. Determine the exact offset to EIP\n")
            self.response_text.insert('end', "3. Craft a payload with the correct offset\n")
            self.response_text.insert('end', "4. Test the payload in a controlled environment")
            self.response_text.configure(state='disabled')
            
            self.console.configure(state='normal')
            self.console.insert('end', "AI inference completed. Response displayed.\n")
            self.console.see('end')
            self.console.configure(state='disabled')
    
    def submit_query(self):
        self.run_inference()
    
    def clear_query(self):
        self.query_text.delete(1.0, 'end')
    
    def run_audit(self):
        if not self.is_running:
            messagebox.showwarning("System Offline", "Please initialize the system first.")
            return
        
        self.console.configure(state='normal')
        self.console.insert('end', "Running security audit...\n")
        self.console.insert('end', "Checking for open ports...\n")
        self.console.insert('end', "Verifying encryption protocols...\n")
        self.console.insert('end', "Validating access controls...\n")
        self.console.insert('end', "Audit complete: No vulnerabilities detected.\n")
        self.console.see('end')
        self.console.configure(state='disabled')
        
        messagebox.showinfo("Security Audit", "Security audit completed successfully. No vulnerabilities detected.")
    
    def show_docs(self):
        doc_window = tk.Toplevel(self.root)
        doc_window.title("Void Ecosystem Documentation")
        doc_window.geometry("800x600")
        doc_window.configure(bg='#0a0a14')
        
        # Add tabs for different documentation sections
        notebook = ttk.Notebook(doc_window, style='Notebook.TNotebook')
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # HLD tab
        hld_frame = ttk.Frame(notebook, style='Frame.TFrame')
        notebook.add(hld_frame, text="High-Level Design")
        
        hld_text = scrolledtext.ScrolledText(hld_frame, bg='#1a1a2e', fg='#ffffff', font=('Consolas', 10))
        hld_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        hld_content = """
        VOID ECOSYSTEM - HIGH LEVEL DESIGN
        
        System Vision:
        The Void Ecosystem provides an On-Premise, AI-Augmented Cyber Range.
        It solves the "Expert Gap" in cybersecurity education by integrating a 
        context-aware LLM directly into a containerized laboratory environment.
        
        Logical Architecture:
        - Modular Microservices Architecture
        - Intelligence Layer: "Void" (Proprietary)
        - Control Plane: "Void the Hack" (Orchestrator)
        
        Key Components:
        1. Inference Service: gRPC-based microservice hosting specialized LLM
        2. Context Injection Gateway: Middleware that enriches queries with live state data
        3. Knowledge Base: Vector database with OST2, HTB, and RE documentation
        4. API Gateway: Java-based system managing authentication and routing
        5. Lab Manager: Interfaces with Docker to provision environments
        6. Telemetry Engine: Tracks student progress and adjusts hint levels
        
        Network Fabric:
        - Software Defined Perimeter (SDP) using Headscale/WireGuard
        - Virtual Private Clouds (VPC) per student for traffic isolation
        
        Data Flow:
        1. Request Initiation: Student interacts with target binary
        2. State Capture: Platform captures CPU register state or network logs
        3. Synthesis: Context Gateway combines question with captured state
        4. Inference: Void Engine processes the request
        5. Actionable Output: Student receives explanation and non-destructive hint
        
        Performance Targets:
        - Query Latency: < 250ms for standard queries
        - Model: DeepSeek-Coder-V2 Lite (QLoRA)
        - Parameters: 16B (compressed to ~8.5GB)
        - Context Window: 32k tokens
        - VRAM Allocation: 10GB dedicated to APU
        
        Deployment Strategy:
        - Single-Binary Installer (Java)
        - Docker-based ecosystem
        - Zero-Config experience
        """
        
        hld_text.insert('end', hld_content)
        hld_text.configure(state='disabled')
        
        # PoC tab
        poc_frame = ttk.Frame(notebook, style='Frame.TFrame')
        notebook.add(poc_frame, text="Proof of Concept")
        
        poc_text = scrolledtext.ScrolledText(poc_frame, bg='#1a1a2e', fg='#ffffff', font=('Consolas', 10))
        poc_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        poc_content = """
        VOID ECOSYSTEM - PROOF OF CONCEPT
        
        Technical Implementation:
        
        System Architecture:
        - Core Engine: DeepSeek-Coder-V2 Lite (QLoRA)
        - Orchestrator: Java 21 / Docker Java API
        - Network Mesh: Headscale + WireGuard
        - Frontend: HTML5/CSS3/JS (via WebView)
        
        VRAM Allocation:
        - Model Weight Management: 16B parameters compressed to ~8.5GB
        - Context Window: 32k tokens
        - Offloading: 100% of KV Cache and Model Weights in allocated VRAM
        
        Infrastructure Workflow:
        1. Handshake: Java Installer checks for WSL2/Docker
        2. Mesh Initialization: Headscale deployed in Docker container
        3. Tunneling: Laptop connects via WireGuard mesh
        4. Courseware Injection: Void parses current module for real-time hints
        
        Verification Metrics:
        - Inference Speed: > 8 tokens/sec on Ryzen 5600G
        - Latency: < 100ms for command execution
        - Resource Ceiling: System RAM < 14GB
        - Security: Zero open ports to WAN
        
        Licensing:
        - Void (Proprietary): Specific weights and Context-Injection logic
        - Void the Hack (FOSS): UI wrapper, Docker scripts, Headscale orchestration
        """
        
        poc_text.insert('end', poc_content)
        poc_text.configure(state='disabled')
    
    def show_component_diagram(self):
        diagram_window = tk.Toplevel(self.root)
        diagram_window.title("Context Injection Gateway - Component Diagram")
        diagram_window.geometry("800x600")
        diagram_window.configure(bg='#0a0a14')
        
        title_label = ttk.Label(diagram_window, text="Context Injection Gateway Component Diagram", style='Subtitle.TLabel')
        title_label.pack(pady=10)
        
        canvas = tk.Canvas(diagram_window, bg='#1a1a2e', highlightthickness=0)
        canvas.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Draw component diagram
        components = [
            ("Student UI", 400, 100, 150, 60, '#123456'),
            ("Context Gateway", 400, 200, 150, 60, '#561234'),
            ("State Capture", 250, 200, 120, 60, '#345612'),
            ("Void AI Engine", 400, 300, 150, 60, '#125634'),
            ("Knowledge Base", 550, 300, 120, 60, '#563412')
        ]
        
        for name, x, y, w, h, color in components:
            canvas.create_rectangle(x-w/2, y-h/2, x+w/2, y+h/2, fill=color, outline='#ffffff', width=2)
            canvas.create_text(x, y, text=name, fill='white', font=('Consolas', 10))
        
        # Draw connections
        canvas.create_line(400, 100+30, 400, 200-30, fill='#00ff00', width=2, arrow=tk.LAST)
        canvas.create_line(250, 200, 400-75, 200, fill='#00ff00', width=2, arrow=tk.LAST)
        canvas.create_line(400, 200+30, 400, 300-30, fill='#00ff00', width=2, arrow=tk.LAST)
        canvas.create_line(400+75, 300, 550, 300, fill='#00ff00', width=2, arrow=tk.LAST)
        canvas.create_line(550, 300, 400, 300, fill='#00ff00', width=2, arrow=tk.LAST)
        
        # Add labels
        canvas.create_text(400, 150, text="User Query", fill='#ffffff', font=('Consolas', 8))
        canvas.create_text(325, 200, text="Live State Data", fill='#ffffff', font=('Consolas', 8))
        canvas.create_text(400, 250, text="Enriched Query", fill='#ffffff', font=('Consolas', 8))
        canvas.create_text(475, 300, text="Retrieve Context", fill='#ffffff', font=('Consolas', 8))
        canvas.create_text(475, 320, text="Store Context", fill='#ffffff', font=('Consolas', 8))
        
        desc_frame = ttk.Frame(diagram_window, style='Frame.TFrame')
        desc_frame.pack(fill='x', padx=10, pady=10)
        
        desc_text = """
        The Context Injection Gateway intercepts user queries and enriches them with live state data
        (e.g., current debugger output or network scan results) before sending them to the AI engine.
        This allows the AI to provide context-aware responses specific to the student's current lab environment.
        """
        
        desc_label = ttk.Label(desc_frame, text=desc_text, style='Status.TLabel', justify='center')
        desc_label.pack(pady=5)
    
    def snapshot_lab(self):
        selection = self.lab_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a lab to snapshot.")
            return
        
        item = self.lab_tree.item(selection[0])
        lab_id = item['values'][0]
        
        self.console.configure(state='normal')
        self.console.insert('end', f"Taking snapshot of lab {lab_id}...\n")
        self.console.insert('end', "Snapshot saved for later restoration.\n")
        self.console.see('end')
        self.console.configure(state='disabled')
    
    def terminate_lab(self):
        selection = self.lab_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a lab to terminate.")
            return
        
        item = self.lab_tree.item(selection[0])
        lab_id = item['values'][0]
        
        self.console.configure(state='normal')
        self.console.insert('end', f"Terminating lab {lab_id}...\n")
        self.console.insert('end', "All containers stopped and removed.\n")
        self.console.see('end')
        self.console.configure(state='disabled')
        
        self.lab_tree.delete(selection[0])
        self.active_labs -= 1
        
        self.lab_details.configure(state='normal')
        self.lab_details.delete(1.0, 'end')
        self.lab_details.insert('end', "Select a lab to view details...")
        self.lab_details.configure(state='disabled')
    
    def reset_lab(self):
        selection = self.lab_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a lab to reset.")
            return
        
        item = self.lab_tree.item(selection[0])
        lab_id = item['values'][0]
        
        self.console.configure(state='normal')
        self.console.insert('end', f"Resetting lab {lab_id} to initial state...\n")
        self.console.insert('end', "Lab reset completed.\n")
        self.console.see('end')
        self.console.configure(state='disabled')
    
    def quick_lab(self):
        # Deploy a lab with default settings
        self.deploy_lab()
    
    def run_diagnostics(self):
        self.console.configure(state='normal')
        self.console.insert('end', "Running system diagnostics...\n")
        self.console.insert('end', "Checking AI service... OK\n")
        self.console.insert('end', "Checking container runtime... OK\n")
        self.console.insert('end', "Checking network mesh... OK\n")
        self.console.insert('end', "All diagnostics passed.\n")
        self.console.see('end')
        self.console.configure(state='disabled')
    
    def check_updates(self):
        self.console.configure(state='normal')
        self.console.insert('end', "Checking for updates...\n")
        self.console.insert('end', "Void Ecosystem is up to date.\n")
        self.console.see('end')
        self.console.configure(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = VoidEcosystemGUI(root)
    root.mainloop()
