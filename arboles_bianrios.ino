const int ledRojo = 2;
const int ledVerde = 4;
const int ledAzul = 6;
const int potenciometro = A3;
int valorPotenciometro;

struct Nodo {
  int valor;
  Nodo* izquierda;
  Nodo* derecha;
};

class ArbolBinario {
public:
  Nodo* raiz;

  ArbolBinario() {
    raiz = nullptr;
  }

  void encenderRojo() {
    digitalWrite(ledRojo, HIGH);
    digitalWrite(ledVerde, LOW);
    digitalWrite(ledAzul, LOW);
  }

  void encenderVerde() {
    digitalWrite(ledRojo, LOW);
    digitalWrite(ledVerde, HIGH);
    digitalWrite(ledAzul, LOW);
  }

  void encenderAzul() {
    digitalWrite(ledRojo, LOW);
    digitalWrite(ledVerde, LOW);
    digitalWrite(ledAzul, HIGH);
  }

  void preorden(Nodo* nodo) {
    if (nodo == NULL) return;
    encenderRojo();
    delay(500);
    Serial.print(nodo->valor);
    Serial.print(" ");
    encenderVerde();
    delay(500);
    preorden(nodo->izquierda);
    preorden(nodo->derecha);
  }

  void inorden(Nodo* nodo) {
    if (nodo == NULL) return;
    inorden(nodo->izquierda);
    encenderAzul();
    delay(500);
    Serial.print(nodo->valor);
    Serial.print(" ");
    encenderVerde();
    delay(500);
    inorden(nodo->derecha);
  }

  void postorden(Nodo* nodo) {
    if (nodo == NULL) return;
    postorden(nodo->izquierda);
    postorden(nodo->derecha);
    encenderRojo();
    delay(500);
    Serial.print(nodo->valor);
    Serial.print(" ");
    encenderAzul();
    delay(500);
  }
};

const int botonA = 10;
const int botonB = 11;
const int botonC = 12;
const int potPin = A3;

void setup() {
  pinMode(ledRojo, OUTPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(ledAzul, OUTPUT);
  pinMode(botonA, INPUT_PULLUP);
  pinMode(botonB, INPUT_PULLUP);
  pinMode(botonC, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  valorPotenciometro = analogRead(potenciometro);
  Serial.print("Valor del potenciómetro: ");
  Serial.println(valorPotenciometro);
  delay(100);

  int sensorValue = analogRead(potPin);
  Serial.println(sensorValue);
  delay(100);

  if (digitalRead(botonA) == LOW || Serial.available() > 0 && Serial.read() == 'A') {
    ArbolBinario arbolA;
    arbolA.raiz = new Nodo();
    arbolA.raiz->valor = 1;
    arbolA.raiz->izquierda = new Nodo();
    arbolA.raiz->izquierda->valor = 2;
    arbolA.raiz->derecha = new Nodo();
    arbolA.raiz->derecha->valor = 3;
    arbolA.preorden(arbolA.raiz);
    delay(1000);
  }

  if (digitalRead(botonB) == LOW || Serial.available() > 0 && Serial.read() == 'B') {
    ArbolBinario arbolB;
    arbolB.raiz = new Nodo();
    arbolB.raiz->valor = 4;
    arbolB.raiz->izquierda = new Nodo();
    arbolB.raiz->izquierda->valor = 5;
    arbolB.raiz->derecha = new Nodo();
    arbolB.raiz->derecha->valor = 6;
    arbolB.inorden(arbolB.raiz);
    delay(1000);
  }

  if (digitalRead(botonC) == LOW || Serial.available() > 0 && Serial.read() == 'C') {
    ArbolBinario arbolC;
    arbolC.raiz = new Nodo();
    arbolC.raiz->valor = 7;
    arbolC.raiz->izquierda = new Nodo();
    arbolC.raiz->izquierda->valor = 8;
    arbolC.raiz->derecha = new Nodo();
    arbolC.raiz->derecha->valor = 9;
    arbolC.postorden(arbolC.raiz);
    delay(1000);
  }
}