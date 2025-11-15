import yaml
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    """Dirección de movimiento del cabezal"""
    L = "L"  # Left
    R = "R"  # Right
    S = "S"  # Stay

@dataclass
class Transition:
    """Representa una transición de la MT"""
    state: str
    read: List[str]
    write: List[str]
    move: str
    next: str

class TuringMachine:
    """Simulador de Máquina de Turing de una cinta"""
    
    def __init__(self, config: Dict):
        """
        Inicializa la MT con la configuración del YAML
        
        Args:
            config: Diccionario con la configuración de la MT
        """
        mt = config['mt']
        self.states = mt['states']
        self.input_alphabet = mt['input_alphabet']
        self.tape_alphabet = mt['tape_alphabet']
        self.initial_state = mt['initial_state']
        self.accept_states = mt['accept_states']
        self.transitions = self._parse_transitions(mt['transitions'])
        
        # Cinta y estado actual
        self.tape: List[str] = []
        self.head_position = 0
        self.current_state = self.initial_state
        
    def _parse_transitions(self, transitions_list: List[Dict]) -> Dict[Tuple, Transition]:
        """
        Parsea las transiciones del YAML a un diccionario
        
        Args:
            transitions_list: Lista de transiciones del YAML
            
        Returns:
            Diccionario con clave (estado, símbolo_leído) -> Transition
        """
        transitions = {}
        for t in transitions_list:
            trans = Transition(
                state=t['state'],
                read=t['read'],
                write=t['write'],
                move=t['move'],
                next=t['next']
            )
            # Para MT de una cinta, tomamos el primer elemento
            key = (trans.state, trans.read[0])
            transitions[key] = trans
        return transitions
    
    def _initialize_tape(self, input_string: str):
        """
        Inicializa la cinta con el input
        
        Args:
            input_string: Cadena de entrada
        """
        self.tape = list(input_string) if input_string else ['B']
        self.head_position = 0
        self.current_state = self.initial_state
    
    def _get_tape_content(self) -> str:
        """
        Obtiene el contenido actual de la cinta
        
        Returns:
            String representando la cinta
        """
        # Eliminar blancos al final para mejor visualización
        tape_str = ''.join(self.tape).rstrip('B')
        if not tape_str:
            return 'B'
        return tape_str
    
    def _get_instantaneous_description(self) -> str:
        """
        Genera la descripción instantánea (ID) actual
        
        Returns:
            String con formato: contenido_izquierda + estado + contenido_derecha
        """
        left = ''.join(self.tape[:self.head_position])
        if self.head_position < len(self.tape):
            right = ''.join(self.tape[self.head_position:])
        else:
            right = 'B'
        
        # Formato: w1 q w2 donde el cabezal está en el primer símbolo de w2
        if not left:
            left = ''
        if not right:
            right = 'B'
            
        return f"{left}[{self.current_state}]{right}"
    
    def _extend_tape_if_needed(self):
        """Extiende la cinta con blancos si el cabezal se sale"""
        while self.head_position >= len(self.tape):
            self.tape.append('B')
        if self.head_position < 0:
            self.tape.insert(0, 'B')
            self.head_position = 0
    
    def _step(self) -> bool:
        """
        Ejecuta un paso de la MT
        
        Returns:
            True si se pudo ejecutar la transición, False si no hay transición aplicable
        """
        self._extend_tape_if_needed()
        
        current_symbol = self.tape[self.head_position]
        key = (self.current_state, current_symbol)
        
        if key not in self.transitions:
            return False
        
        transition = self.transitions[key]
        
        # Escribir en la cinta
        self.tape[self.head_position] = transition.write[0]
        
        # Mover el cabezal
        if transition.move == 'R':
            self.head_position += 1
        elif transition.move == 'L':
            self.head_position -= 1
        # Si es 'S', no se mueve
        
        # Cambiar de estado
        self.current_state = transition.next
        
        return True
    
    def simulate(self, input_string: str, max_steps: int = 10000) -> Tuple[bool, List[str]]:
        """
        Simula la ejecución de la MT con una cadena de entrada
        
        Args:
            input_string: Cadena de entrada
            max_steps: Número máximo de pasos para evitar loops infinitos
            
        Returns:
            Tupla (aceptado, lista_de_IDs)
        """
        self._initialize_tape(input_string)
        ids = [self._get_instantaneous_description()]
        
        steps = 0
        # 👉 Detener si estamos en un estado de aceptación
        while steps < max_steps and self.current_state not in self.accept_states:
            if not self._step():
                # No hay transición aplicable, la MT se detiene
                break
            ids.append(self._get_instantaneous_description())
            steps += 1
        
        accepted = self.current_state in self.accept_states
        return accepted, ids
    
    def print_simulation(self, input_string: str):
        """
        Imprime la simulación de forma legible
        
        Args:
            input_string: Cadena de entrada
        """
        print(f"\n{'='*70}")
        print(f"Simulando entrada: '{input_string}'")
        print(f"{'='*70}")
        
        accepted, ids = self.simulate(input_string)
        
        print("\nDescripciones Instantáneas:")
        print("-" * 70)
        for i, id_str in enumerate(ids):
            print(f"Paso {i}: {id_str}")
        
        print("-" * 70)
        if accepted:
            print(f"✓ CADENA ACEPTADA")
        else:
            print(f"✗ CADENA RECHAZADA")
        print(f"Estado final: {self.current_state}")
        print(f"Contenido final de la cinta: {self._get_tape_content()}")
        print(f"{'='*70}\n")

def load_config(filename: str) -> Dict:
    """
    Carga la configuración desde un archivo YAML
    
    Args:
        filename: Nombre del archivo YAML
        
    Returns:
        Diccionario con la configuración
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    """Función principal para ejecutar el simulador"""
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python turing_machine.py <archivo_config.yaml>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    try:
        config = load_config(config_file)
        tm = TuringMachine(config)
        
        print("\n" + "="*70)
        print("SIMULADOR DE MÁQUINA DE TURING")
        print("="*70)
        print(f"\nEstados: {tm.states}")
        print(f"Alfabeto de entrada: {tm.input_alphabet}")
        print(f"Alfabeto de cinta: {tm.tape_alphabet}")
        print(f"Estado inicial: {tm.initial_state}")
        print(f"Estados de aceptación: {tm.accept_states}")
        print(f"Número de transiciones: {len(tm.transitions)}")
        
        # Simular todas las entradas
        for input_str in config.get('inputs', []):
            tm.print_simulation(input_str)
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{config_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()