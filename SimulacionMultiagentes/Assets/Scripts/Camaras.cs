using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Camaras : MonoBehaviour
{   
    private void Start() {
        cam2.enabled = false;
        cam3.enabled = false;
        StartCoroutine(CambiarCamaras());
    }
    public Camera cam1, cam2, cam3;
    private IEnumerator CambiarCamaras(){
        
        while (true){
            yield return new WaitForSeconds(7);
            cam1.enabled = false;
            cam2.enabled = true;
            yield return new WaitForSeconds(7);
            cam2.enabled = false;
            cam3.enabled = true;
            yield return new WaitForSeconds(7);
            cam3.enabled = false;
            cam1.enabled = true;
        }
    }
}
