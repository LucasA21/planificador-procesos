"""
Componente para la entrada de parámetros del sistema.
"""

import customtkinter as ctk

class EntradaParametros(ctk.CTkFrame):
    """Componente para entrada de parámetros del sistema."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, corner_radius=10, **kwargs)
        
        self.entradas = {}
        self.callback_cambio_parametro = None
        
        self._crear_widgets()
        self._configurar_valores_default()
    
    def _crear_widgets(self):
        """Crea los widgets del componente."""
        # Título de sección
        titulo = ctk.CTkLabel(
            self, 
            text="PARAMETROS DEL SISTEMA", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=(15, 15), padx=15)
        
        # Parámetros del sistema
        self._crear_entrada_parametro("TIP (Tiempo Ingreso Proceso):", "tip", 1)
        self._crear_entrada_parametro("TFP (Tiempo Fin Proceso):", "tfp", 2)
        self._crear_entrada_parametro("TCP (Tiempo Conmutacion):", "tcp", 3)
        self._crear_entrada_parametro("Quantum (solo RR):", "quantum", 4)
    
    def _crear_entrada_parametro(self, texto_label, nombre_param, fila):
        """Crea una entrada de parámetro con label."""
        # Label del parámetro
        label = ctk.CTkLabel(
            self, 
            text=texto_label, 
            font=ctk.CTkFont(size=12)
        )
        label.grid(row=fila, column=0, pady=(10, 5), padx=15, sticky="w")
        
        # Entrada del parámetro
        entrada = ctk.CTkEntry(
            self, 
            height=30
        )
        entrada.grid(row=fila, column=0, pady=(0, 10), padx=15, sticky="ew")
        
        # Guardar referencia y configurar callback
        self.entradas[nombre_param] = entrada
        entrada.bind('<KeyRelease>', lambda e: self._cambio_parametro(nombre_param))
    
    def _configurar_valores_default(self):
        """Configura valores por defecto para los parámetros."""
        valores_default = {
            "tip": "1",
            "tfp": "1", 
            "tcp": "1",
            "quantum": "2"
        }
        
        for nombre_param, valor in valores_default.items():
            self.entradas[nombre_param].insert(0, valor)
    
    def _cambio_parametro(self, nombre_param):
        """Maneja el cambio de un parámetro."""
        if self.callback_cambio_parametro:
            self.callback_cambio_parametro(nombre_param, self.obtener_valor_parametro(nombre_param))
    
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
            estado = "normal" if habilitar else "disabled"
            self.entradas["quantum"].configure(state=estado)
    
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
