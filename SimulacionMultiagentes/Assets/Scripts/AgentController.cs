using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AgentController : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        // robotsData = new RobotsData();
        // boxesData = new BoxesData();
        // palletsData = new PalletsData();

        // prevPositions = new Dictionary<string, Vector3>();
        // currPositions = new Dictionary<string, Vector3>();

        // boxes = new Dictionary<string, GameObject>();
        // robots = new Dictionary<string, GameObject>();
        // pallets = new Dictionary<string, GameObject>();

        // // Escalar y posicionar piso
        // floor.transform.localScale = new Vector3((float)(width + 1) / 10, 1, (float)(height + 1) / 10);
        // floor.transform.localPosition = new Vector3((float)width / 2 - 0.5f, 0, (float)height / 2 - 0.5f);

        // timer = timeToUpdate;

        // StartCoroutine(SendConfiguration());
    }

    // Update is called once per frame
    
    IEnumerator SendConfiguration()
    {
        // WWWForm form = new WWWForm();

        // form.AddField("NAgents", (NBoxes).ToString());
        // form.AddField("width", (width).ToString());
        // form.AddField("height", (height).ToString());
        // form.AddField("maxSteps", (maxSteps).ToString());

        // UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        // www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        // yield return www.SendWebRequest();

        // if (www.result != UnityWebRequest.Result.Success)
        // {
        //     Debug.Log(www.error);
        // }
        // // Empezar simulación si hay conexión exitosa
        // else
        // {
        //     //Debug.Log("Configuration upload complete!");
        //     //Debug.Log("Getting Agents positions");
        //     StartCoroutine(GetRobotsData());
        //     StartCoroutine(GetBoxesData());
        //     StartCoroutine(GetPalletsData());
        // }
        yield return 0;
    }
    void Update()
    {
        // if(timer < 0)
        // {
        //     timer = timeToUpdate;
        //     updated = false;
        //     StartCoroutine(UpdateSimulation());
        // }

        // if (updated)
        // {
        //     timer -= Time.deltaTime;
        //     dt = 1.0f - (timer / timeToUpdate);

        //     foreach(var rob in currPositions)
        //     {
        //         Vector3 currentPosition = rob.Value;
        //         Vector3 previousPosition = prevPositions[rob.Key];

        //         Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
        //         Vector3 direction = currentPosition - interpolated;

        //         robots[rob.Key].transform.localPosition = interpolated;
        //         // Cambiar hacia dónde miran los robots dependiendo de su posición y dirección
        //         if (direction != Vector3.zero) robots[rob.Key].transform.rotation = Quaternion.LookRotation(direction);
        //     }
        // }
    }

    IEnumerator UpdateSimulation()
    {
    //     UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
    //     yield return www.SendWebRequest();
 
    //     if (www.result != UnityWebRequest.Result.Success)
    //         Debug.Log(www.error);
    //     else 
    //     {
    //         StartCoroutine(GetRobotsData());
    //         StartCoroutine(GetBoxesData());
    //         StartCoroutine(GetPalletsData());
    //     }
    yield return 0;
    }
}
