# Dependency Injection

## Introduzione

### Il problema delle dipendenze

Si consideri la seguente classe:
```csharp
public class Car
{
  private readonly PetrolEngine _engine = new PetrolEngine();
  public void StartEngine(){
    _engine.Start();
  }

}

public class PetrolEngine{
  public void Start(){
    Console.WriteLine("Starting the Petrol Engine...");
    MixPetrolAndAir();
    InjectMixture();
    IgniteBySpark();
  }
}
```
Come si può vedere, l'oggetto `Car` dipende interamente nella sua implementazione da `PetrolEngine`: nel caso in cui si volesse cambiare tipo di motore (es. Diesel), bisognerebbe creare una nuova classe `DieselEngine`:
```csharp
public class DieselEngine{
  public void Start(){
    Console.WriteLine("Starting the Diesel Engine...");
    // Do stuff to start the Diesel Engine
  }
}
```
E usare quella nell'oggetto `Car`, di fatto rendendomi la classe interamente dipendente dal tipo di motore che implementa (ovvero sarebbe una `DieselCar` o una `PetrolCar`, ma non una generica `Car`).

In più, in assenza di un'instanziazione di `PetrolEngine`, l'oggetto `Car` non può nemmeno essere instanziato e quindi non può nemmeno essere testato per altre funzioni che non dipendano dall'esistenza di un motore.


### Necessità della Dependency Injection

Questo succede perché la classe `Car` non dovrebbe dipendere da implementazioni (`private readonly PetrolEngine _engine = new PetrolEngine();` oppure `private readonly DieselEngine _engine = new DieselEngine();`), ma da astrazioni - ovvero, interfacce.

Aggiungiamo quindi l'interfaccia per il 'generico' motore:
```csharp
public interface ICarEngine
{
    void Start();
}
```
Di cui i motori precedenti diventano implementazioni:
```csharp
public class PetrolEngine : ICarEngine
{
  public void Start()
  {
    Console.WriteLine("Starting the Petrol Engine...");
    // Do stuff to start the Petrol Engine
  }
}

public class DieselEngine : ICarEngine
{
  public void Start()
  {
    Console.WriteLine("Starting the Diesel Engine...");
    // Do stuff to start the Diesel Engine
  }
}
```
Quindi l'implementazione hard-coded scritta sopra (`private readonly PetrolEngine _engine = new PetrolEngine();`) diventa l'implementazione di un'interfaccia, ovvero:
```csharp
public class Car
{  
  // instantiate the interface  
  private readonly ICarEngine _carEngine;

  // constructor, including the engine
  public Car(ICarEngine carEngine){
    _carEngine = carEngine;
  }

  // the rest ... ...
  public void StartEngine(){
    _engine.Start();
  }  
}
```
In questa maniera, possiamo implementare separatamente la `PetrolCar` e la `DieselCar` o qualsiasi altra `*Car` semplicemente chiamando la classe astratta `Car` e passando il tipo di motore nel costruttore, avvantaggiandosi dell'interfaccia appena aggiunta:
```csharp
// Start car with petrol engine
Car petrolCar = new Car(new PetrolEngine());
petrolCar.StartEngine();

// Start car with diesel engine
Car dieselEngine = new Car(new DieselEngine());
petrolCar.StartEngine();
```
Potrei anche creare un tipo di motore finto, necessario giusto per testare altre parti della classe `Car` e risolvendo il problema di testabilità citato prima:
```csharp
// Virtual engine
public class TestEngine : ICarEngine
{
    public void Start(){
        Console.WriteLine("Starting a test engine...");
    };
}
```