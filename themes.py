CORES_MICROCONTROLADORES = {
    "Raspberry": "#C51A4A",   # vermelho raspberry (oficial)
    "Arduino": "#00979D",     # verde água oficial Arduino
    "PIC": "#6f42c1",         # roxo escuro (tecnológico)
    "STM": "#1c7ed6",         # azul forte (industrial)
    "Attiny": "#e67700",      # laranja queimado (diferente do Arduino)
} 

CORES_ARMAZENAMENTO = {
    "PenDrive": "#495057",   # cinza escuro (hardware)
    "MicroSD": "#868e96",    # cinza mais claro (variação)
} 

CORES_EXTRA = {
    "Adaptador": "#74c0fc",     # azul claro
    "Diodo": "#fa5252",         # vermelho
    "Diodo Zener": "#ff6b6b",   # vermelho mais claro
}

CORES_TIPO = {
    "Resistor": "#ffd43b",
    "Capacitor": "#ffa94d",
    "Varistor": "#ff922b",
    "Itens para placa": "#fff3bf",
    "Acessórios": "#adb5bd",
    "Conectores": "#c92a2a",
    "Baterias": "#f76707",
    "Displays": "#faa2c1",
    "Relé": "#8ce99a",
    "Protoboard": "#dee2e6",
    "Fusíveis": "#ff922b",
    "LED": "#ffffff",
    "Transistor": "#fd7e14",
    "CI": "#ff922b",
    "Módulo": "#f3d9fa",
    "Módulo sensor": "#cc5de8",
}

CORES_CAIXA = {
    "Caixa de resistores": "#fff176",
    "Caixa de capacitor": "#ffcc80",
    "Caixa de itens para placa": "#fff9c4",
    "Caixa dos conectores": "#8b0000",
    "Caixa de baterias": "#ff8f00",
    "Caixa dos displays": "#f8bbd0",
    "Caixa do relé": "#ccff90",
    "Caixa da protoboard": "#f1f3f5",
    "Caixa fusíveis": "#ffa94d",
    "Caixa LED": "#ffffff",
    "Caixa TR": "#4dabf7",
    "Caixa módulo": "#f5e6ca",
    "Caixa microcontroladores": "#d3f9d8",
    "Caixa raspberry/arduino": "#e5dbff",
    "Caixa LoRa": "#99e9f2",
}

def cor_por_categoria(tipo: str) -> str:
    tipo = tipo.strip()

    if tipo in CORES_MICROCONTROLADORES:
        return CORES_MICROCONTROLADORES[tipo]

    if tipo in CORES_ARMAZENAMENTO:
        return CORES_ARMAZENAMENTO[tipo]

    if tipo in CORES_EXTRA:
        return CORES_EXTRA[tipo]

    return CORES_TIPO.get(tipo, "#ced4da")