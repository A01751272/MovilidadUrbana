using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

[Serializable] 
public class CarData
{
    public string id;
    public float x, y, z;

    public CarData(string id, float x, float y, float z){
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
    }
}

[Serializable]
public class CarsData
{
    public List<CarData> positions;

    public CarsData() => this.positions = new List<CarData>();
}

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

public class AgentController : MonoBehaviour
{
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

    bool carUpdated = false, carStarted = false;
    bool tlightStarted = false;

    public GameObject carro, semaforo;
     public int InitialCars, CarsEvery, MaxSteps;
     public float timeToUpdate;
    private float timer, dt;
    // Start is called before the first frame update
    void Start()
    {
        carsData = new CarsData();
        tlightsData = new TLightsData();

        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();

        cars = new Dictionary<string, GameObject>();
        lights = new Dictionary<string, GameObject>();
        timer = timeToUpdate;
        StartCoroutine(SendConfiguration());
    }

    // Update is called once per frame
    
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
            //StartCoroutine(GetBoxesData());
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

                // Instanciar carros
                if (!existentes.ContainsKey(car.id))
                {
                    prevPositions[car.id] = newAgentPosition;
                    cars[car.id] = Instantiate(carro, newAgentPosition, carro.transform.rotation);
                    existentes[car.id] = true;
                }
                // Si el carro ya existe, modificar su comportamiento y apariencia
                else
                {
                    Vector3 currentPosition = new Vector3();
                    if (currPositions.TryGetValue(car.id, out currentPosition))
                        prevPositions[car.id] = currentPosition;
                    currPositions[car.id] = newAgentPosition;
                }
            }
            carUpdated = true;
            if (!carStarted) carStarted = true;
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
                // Cambiar hacia dónde miran los robots dependiendo de su posición y dirección
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
            //StartCoroutine(GetBoxesData());
        }
    yield return 0;
    }
}
