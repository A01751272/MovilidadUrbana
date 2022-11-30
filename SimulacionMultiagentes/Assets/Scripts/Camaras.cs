// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// Código en C# para cambiar la cámara principal durante la simulación
// Pablo González, Humberto Romero, Valeria Martínez y Aleny Arévalo
// Última modificación 29 de Noviembre 2022

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Camaras : MonoBehaviour
{   
    // Cáamaras a usar
    public Camera cam1, cam2, cam3;
    private void Start() {
        cam2.enabled = false;
        cam3.enabled = false;
        StartCoroutine(CambiarCamaras());
    }
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
