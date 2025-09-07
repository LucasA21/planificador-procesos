"""
Componente para la entrada de parámetros del sistema.
"""

import customtkinter as ctk
import tkinter as tk

class EntradaParametros(ctk.CTkFrame):
    """Componente para entrada de parámetros del sistema."""
    
    def __init__(self, parent, factor_escala=1.0, **kwargs):
        super().__init__(parent, corner_radius=15, fg_color="transparent", **kwargs)
        
        self.factor_escala = factor_escala
        self.entradas = {}
        self.indicadores = {}
        self.callback_cambio_parametro = None
        
        # Configurar grid para que ocupe todo el ancho
        self.grid_columnconfigure(0, weight=1)
        
        self._crear_widgets()
        self._configurar_valores_default()
    
    def _crear_widgets(self):
        """Crea los widgets del componente."""
        # Frame principal con borde y sombra
        main_frame = ctk.CTkFrame(
            self,
            corner_radius=int(15 * self.factor_escala),
            border_width=1
        )
        main_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Título de sección con icono visual
        titulo_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=int(40 * self.factor_escala))
        titulo_frame.grid(row=0, column=0, sticky="ew", padx=int(20 * self.factor_escala), pady=(int(20 * self.factor_escala), int(20 * self.factor_escala)))
        titulo_frame.grid_columnconfigure(0, weight=1)
        
        titulo = ctk.CTkLabel(
            titulo_frame, 
            text="Parámetros del Sistema",
            font=ctk.CTkFont(size=int(16 * self.factor_escala), weight="bold")
        )
        titulo.grid(row=0, column=0, sticky="w")
        
        # Parámetros del sistema
        self._crear_entrada_parametro("TIP (Tiempo Ingreso Proceso):", "tip", 1, main_frame)
        self._crear_entrada_parametro("TFP (Tiempo Fin Proceso):", "tfp", 2, main_frame)
        self._crear_entrada_parametro("TCP (Tiempo Conmutación):", "tcp", 3, main_frame)
        self._crear_entrada_parametro("Quantum (solo RR):", "quantum", 4, main_frame)
    
    def _crear_entrada_parametro(self, texto_label, nombre_param, fila, parent):
        """Crea una entrada de parámetro con label e indicador de validación."""
        # Frame para cada parámetro
        param_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            height=int(70 * self.factor_escala)
        )
        param_frame.grid(row=fila, column=0, sticky="ew", padx=int(20 * self.factor_escala), pady=(0, int(15 * self.factor_escala)))
        param_frame.grid_columnconfigure(0, weight=1)
        
        # Label del parámetro
        label = ctk.CTkLabel(
            param_frame, 
            text=texto_label, 
            font=ctk.CTkFont(size=int(13 * self.factor_escala), weight="bold")
        )
        label.grid(row=0, column=0, pady=(int(15 * self.factor_escala), int(8 * self.factor_escala)), padx=0, sticky="w")
        
        # Frame para entrada e indicador
        input_frame = ctk.CTkFrame(param_frame, fg_color="transparent")
        input_frame.grid(row=1, column=0, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Entrada del parámetro con diseño moderno
        entrada = ctk.CTkEntry(
            input_frame, 
            height=int(35 * self.factor_escala),
            corner_radius=int(8 * self.factor_escala),
            border_width=1,
            font=ctk.CTkFont(size=int(14 * self.factor_escala)),
            placeholder_text="Ingrese valor..."
        )
        entrada.grid(row=0, column=0, pady=(0, int(15 * self.factor_escala)), sticky="ew")
        
        # Indicador de validación
        indicador = ctk.CTkFrame(
            input_frame,
            width=int(8 * self.factor_escala),
            height=int(8 * self.factor_escala),
            corner_radius=int(4 * self.factor_escala)
        )
        indicador.grid(row=0, column=1, pady=(0, int(15 * self.factor_escala)), padx=(int(8 * self.factor_escala), 0), sticky="e")
        
        # Guardar referencias
        self.entradas[nombre_param] = entrada
        self.indicadores[nombre_param] = indicador
        
        # Configurar callbacks
        entrada.bind('<KeyRelease>', lambda e: self._cambio_parametro(nombre_param))
        entrada.bind('<FocusIn>', lambda e: self._on_focus_in(entrada))
        entrada.bind('<FocusOut>', lambda e: self._on_focus_out(entrada))
        entrada.bind('<Return>', lambda e: self._validar_parametro(nombre_param))
    
    def _on_focus_in(self, entrada):
        """Maneja el evento de focus in."""
        entrada.configure(border_color="blue")
    
    def _on_focus_out(self, entrada):
        """Maneja el evento de focus out."""
        entrada.configure(border_color="gray")
    
    def _validar_parametro(self, nombre_param):
        """Valida un parámetro específico y actualiza su indicador visual."""
        try:
            valor = int(self.entradas[nombre_param].get())
            if valor < 0:
                # Error: valor negativo
                self.indicadores[nombre_param].configure(fg_color="red")
                self.entradas[nombre_param].configure(border_color="red")
            else:
                # Éxito: valor válido
                self.indicadores[nombre_param].configure(fg_color="green")
                self.entradas[nombre_param].configure(border_color="gray")
        except ValueError:
            # Error: no es un número
            self.indicadores[nombre_param].configure(fg_color="red")
            self.entradas[nombre_param].configure(border_color="red")
    
    def _cambio_parametro(self, nombre_param):
        """Maneja el cambio de un parámetro con validación en tiempo real."""
        # Validar el parámetro
        self._validar_parametro(nombre_param)
        
        # Notificar cambio
        if self.callback_cambio_parametro:
            self.callback_cambio_parametro(nombre_param, self.obtener_valor_parametro(nombre_param))
    
    def _configurar_valores_default(self):
        """Configura valores por defecto para los parámetros."""
        # Los campos empiezan vacíos, sin valores por defecto
        # Los usuarios deben ingresar los valores manualmente
        pass
    
    def obtener_valor_parametro(self, nombre_param):
        """Obtiene el valor de un parámetro específico."""
        try:
            return int(self.entradas[nombre_param].get())
        except ValueError:
            return 0
    
    def obtener_todos_parametros(self):
        """Retorna todos los parámetros como un diccionario."""
        return {
            "tip": self.obtener_valor_parametro("tip"),
            "tfp": self.obtener_valor_parametro("tfp"),
            "tcp": self.obtener_valor_parametro("tcp"),
            "quantum": self.obtener_valor_parametro("quantum")
        }
    
    def habilitar_quantum(self, habilitar=True):
        """Habilita o deshabilita el campo quantum."""
        if "quantum" in self.entradas:
            if habilitar:
                self.entradas["quantum"].configure(
                    state="normal"
                )
            else:
                self.entradas["quantum"].configure(
                    state="disabled"
                )
    
    def establecer_callback(self, callback):
        """Establece el callback cuando cambian los parámetros."""
        self.callback_cambio_parametro = callback
    
    def validar_parametros(self):
        """Valida que todos los parámetros sean válidos."""
        for nombre_param, entrada in self.entradas.items():
            try:
                valor = int(entrada.get())
                if valor < 0:
                    return False, f"El parámetro {nombre_param} debe ser positivo"
            except ValueError:
                return False, f"El parámetro {nombre_param} debe ser un número entero"
        
        return True, "Todos los parámetros son válidos"
