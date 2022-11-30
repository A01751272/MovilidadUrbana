// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// Código en C# que interactúa con el servidor en Python. Basado en el código de Sergio Ruiz.
// Adaptado por Pablo González, Humberto Romero, Valeria Martínez y Aleny Arévalo
// Última modificación 29 de Noviembre 2022

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

// Clase del agente carro
[Serializable] 
public class CarData
{
    public string id;
    public float x, y, z;
    public bool reached_destination;

    public CarData(string id, float x, float y, float z, bool reached_destination){
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.reached_destination = reached_destination;
    }
}

[Serializable]
public class CarsData
{
    public List<CarData> positions;

    public CarsData() => this.positions = new List<CarData>();
}

// Clase del agente semáforo
[Serializable]
public class TLightData
{
    public string id;
    public float x, y, z;
    public bool state;

    public TLightData(string id, float x, float y, float z, bool state)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.state = state;
    }
}

[Serializable]
public class TLightsData
{
    public List<TLightData> positions;

    public TLightsData() => this.positions = new List<TLightData>();
}

// Clase que controla el movimiento y visualización de los agentes
public class AgentController : MonoBehaviour
{
    // Endpoints
    string serverUrl = "http://localhost:8585";
    string getCarsEndpoint = "/getCars";
    string getLightsEndpoint = "/getLights";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";

    CarsData carsData;
    TLightsData tlightsData;


    Dictionary<string, GameObject> cars;
    Dictionary<string, GameObject> lights;
    Dictionary<string, Vector3> prevPositions, currPositions;

    Dictionary<string, bool> existentes;

    bool carUpdated = false, tlightStarted = false;

    //Prefabs
    public GameObject carro1, carro2, carro3, carro4, carro5, carro6, carro7, semaforo;
     public int InitialCars, CarsEvery;
     public float timeToUpdate;
    private float timer, dt;
    // Start is called before the first frame update
    void Start()
    {
        // Inicializacion y envio de datos iniciales 
        carsData = new CarsData();
        tlightsData = new TLightsData();

        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();

        existentes = new Dictionary<string, bool>();

        cars = new Dictionary<string, GameObject>();
        lights = new Dictionary<string, GameObject>();
        timer = timeToUpdate;
        StartCoroutine(SendConfiguration());
    }

    // Funcion para enviar la configuración inicial    
    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("InitialCars", (InitialCars).ToString());
        form.AddField("CarsEvery", (CarsEvery).ToString());
        //form.AddField("MaxSteps", (MaxSteps).ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        // Empezar simulación si hay conexión exitosa
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            StartCoroutine(GetCarsData());
            StartCoroutine(GetLightsData());
        }
        yield return 0;
    }

IEnumerator GetCarsData()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getCarsEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            carsData = JsonUtility.FromJson<CarsData>(www.downloadHandler.text);

            foreach (CarData car in carsData.positions)
            {
                Vector3 newAgentPosition = new Vector3(car.x, car.y, car.z);

                // Instanciar carros si es que no existen
                if (!existentes.ContainsKey(car.id))
                {
                    prevPositions[car.id] = newAgentPosition;
                    int n = UnityEngine.Random.Range(1, 8);
                    switch(n){
                        case 1:
                            cars[car.id] = Instantiate(carro1, newAgentPosition, carro1.transform.rotation);
                            break;
                        case 2:
                            cars[car.id] = Instantiate(carro2, newAgentPosition, carro2.transform.rotation);
                            break;
                        case 3:
                            cars[car.id] = Instantiate(carro3, newAgentPosition, carro3.transform.rotation);
                            break;
                        case 4:
                            cars[car.id] = Instantiate(carro4, newAgentPosition, carro4.transform.rotation);
                            break;
                        case 5:
                            cars[car.id] = Instantiate(carro5, newAgentPosition, carro5.transform.rotation);
                            break;
                        case 6:
                            cars[car.id] = Instantiate(carro6, newAgentPosition, carro6.transform.rotation);
                            break;
                        case 7:
                            cars[car.id] = Instantiate(carro7, newAgentPosition, carro7.transform.rotation);
                            break;
                    }
                    cars[car.id].name = car.id;
                    existentes[car.id] = true;
                }
                // Si el carro ya existe, modificar su comportamiento y apariencia
                else
                {
                    if (car.reached_destination){
                        Destroy(cars[car.id], timeToUpdate);
                        cars.Remove(car.id);
                        existentes.Remove(car.id);
                        currPositions.Remove(car.id);
                        prevPositions.Remove(car.id);
                    } else {
                        Vector3 currentPosition = new Vector3();
                        if (currPositions.TryGetValue(car.id, out currentPosition))
                            prevPositions[car.id] = currentPosition;
                        currPositions[car.id] = newAgentPosition;
                    }
                }
            }
            carUpdated = true;
        }
    }

    IEnumerator GetLightsData(){
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getLightsEndpoint);
        yield return www.SendWebRequest();
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else{
            tlightsData = JsonUtility.FromJson<TLightsData>(www.downloadHandler.text);

            foreach(TLightData light in tlightsData.positions)
            {
                // Instanciar semaforos
                if (!tlightStarted)
                {
                    Vector3 lightPosition = new Vector3(light.x, light.y, light.z);
                    lights[light.id] = Instantiate(semaforo, lightPosition, Quaternion.identity);
                    lights[light.id].name = light.id;
                }
                // Si el semaforo ya existe, modificar su estado
                else
                {
                    if(light.state){
                        lights[light.id].GetComponent<Light>().color = Color.green;
                    } else {
                        lights[light.id].GetComponent<Light>().color = Color.red;
                    }
                }
            }
            if (!tlightStarted) tlightStarted = true;
        }
    }

    void Update()
    {
        if(timer < 0)
        {
            timer = timeToUpdate;
            carUpdated = false;
            StartCoroutine(UpdateSimulation());
        }

        if (carUpdated)
        {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            foreach(var car in currPositions)
            {
                Vector3 currentPosition = car.Value;
                Vector3 previousPosition = prevPositions[car.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = currentPosition - interpolated;

                cars[car.Key].transform.localPosition = interpolated;
                // Cambiar hacia dónde miran los carros dependiendo de su posición y dirección
                if (direction != Vector3.zero) cars[car.Key].transform.rotation = Quaternion.LookRotation(direction);
            }
        }
    }

    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            StartCoroutine(GetCarsData());
            StartCoroutine(GetLightsData());
        }
    yield return 0;
    }
}
