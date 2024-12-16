class SistemaComponentes:
    def __init__(self):
        # Diccionario para almacenar los componentes y sus estados
        self.componentes = {}
        # Matriz de probabilidades condicionales
        # formato: {(comp_origen, comp_destino): probabilidad}
        self.probabilidades_condicionales = {}

    def agregar_componente(self, nombre, prob_fallo_base):
        """
        Agrega un nuevo componente al sistema
        nombre: identificador del componente
        prob_fallo_base: probabilidad de fallo sin condiciones previas
        """
        self.componentes[nombre] = {
            'fallado': False,
            'prob_base': prob_fallo_base
        }

    def agregar_dependencia(self, comp_origen, comp_destino, prob_condicional):
        """
        Define una dependencia entre componentes
        comp_origen: componente que al fallar afecta a otro
        comp_destino: componente afectado
        prob_condicional: nueva probabilidad de fallo si comp_origen falla
        """
        if 0 <= prob_condicional <= 1:
            self.probabilidades_condicionales[(
                comp_origen, comp_destino)] = prob_condicional
        else:
            raise ValueError("La probabilidad debe estar entre 0 y 1")

    def simular_fallo(self, componente):
        """
        Simula el posible fallo de un componente considerando las dependencias
        Retorna True si el componente falla, False en caso contrario
        """
        import random

        if componente not in self.componentes:
            raise ValueError(f"El componente {componente} no existe")

        # Encontrar componentes que afectan al actual
        prob_fallo = self.componentes[componente]['prob_base']

        for (origen, destino), prob in self.probabilidades_condicionales.items():
            if destino == componente and self.componentes[origen]['fallado']:
                # Si hay un componente del que depende y ha fallado,
                # actualizamos la probabilidad
                prob_fallo = prob
                break

        # Simular el fallo
        if random.random() < prob_fallo:
            self.componentes[componente]['fallado'] = True
            return True
        return False

    def reiniciar_sistema(self):
        """Reinicia el estado de todos los componentes"""
        for comp in self.componentes:
            self.componentes[comp]['fallado'] = False

    def obtener_estado(self):
        """Retorna el estado actual de todos los componentes"""
        return {comp: datos['fallado']
                for comp, datos in self.componentes.items()}

# Ejemplo de uso


def ejemplo_sistema():
    sistema = SistemaComponentes()

    # Agregar componentes con sus probabilidades base de fallo
    sistema.agregar_componente('Fuente de poder', 0.05)
    sistema.agregar_componente('Disco duro', 0.03)
    sistema.agregar_componente('Memoria RAM', 0.02)

    # Definir dependencias
    # Si falla la fuente de poder, el disco tiene 0.8 de prob. de fallar
    sistema.agregar_dependencia('Fuente de poder', 'Disco duro', 0.8)
    # Si falla la fuente de poder, la RAM tiene 0.7 de prob. de fallar
    sistema.agregar_dependencia('Fuente de poder', 'Memoria RAM', 0.7)

    # Simular fallos
    componentes = ['Fuente de poder', 'Disco duro', 'Memoria RAM']
    for comp in componentes:
        if sistema.simular_fallo(comp):
            print(f"¡El componente {comp} ha fallado!")

    print("\nEstado final del sistema:", sistema.obtener_estado())


if __name__ == "__main__":
    ejemplo_sistema()
