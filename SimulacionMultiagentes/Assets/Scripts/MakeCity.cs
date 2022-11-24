using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MakeCity : MonoBehaviour
{
    [SerializeField] TextAsset layout;
    [SerializeField] GameObject roadPrefab;
    [SerializeField] GameObject curvePrefab;
    [SerializeField] GameObject crossPrefab;
    [SerializeField] GameObject emptyPrefab;
    [SerializeField] GameObject building1Prefab;
    [SerializeField] GameObject building2Prefab;
    [SerializeField] GameObject building3Prefab;
    [SerializeField] GameObject building4Prefab;
    [SerializeField] GameObject building5Prefab;
    [SerializeField] GameObject semaphorePrefab;
    [SerializeField] GameObject parkingPrefab;
    [SerializeField] int tileSize;

    //Listas con coordenadas para prefabs especificos
    public List<(int,int)> upLight = new List<(int,int)> {(0,12), (1,12), (6,1), (7,1), (13,1), (14,1)};
    public List<(int,int)> downLight = new List<(int,int)> {(6,15), (7,15), (22, 6), (23, 6), (16,21), (17,21)};
    public List<(int,int)> leftLight = new List<(int,int)> {(5,-1), (5,0), (12,-1), (12,0), (21,8), (21,7)};
    public List<(int,int)> rightLight = new List<(int,int)> {(2,11), (2,10), (8,17), (8,16), (18,22), (18,23)};
    public List<(int,int)> upBuilding = new List<(int,int)> {(2,6), (3,6), (4,6), (5,6), (8,6), (9,6), (10,6), 
    (11,6), (12,6), (15,6), (18,6), (19,6), (20,6), (21,6), (2,9), (3,9), (4,9), (5,9), (6,9), (7,9), (8,9),
    (10,9), (11,9), (14,9), (15,9), (16,9), (19,9), (20,9), (21,9), (2,15), (3,15), (4,15), (5,15), (8,15),
    (9,15), (10,15), (11,15), (12,15), (2,21), (3,21), (4,21), (5,21), (6,21), (7,21), (8,21), (9,21), (10,21),
    (11,21), (12,21), (15,21), (18,21), (19,21), (20,21), (21,21)};
    public List<(int,int)> downBuilding = new List<(int,int)> {(2,1), (3,1), (4,1), (5,1), (8,1), (9,1), (10,1),
    (11,1), (12,1), (15,1), (18,1), (19,1), (20,1), (21,1), (2, 12), (3,12), (4,12), (5,12),(8,12), (9,12), 
    (10,12), (11,12), (12,12), (15,12), (18,12), (19,12), (20,12), (21,12), (2,18), (3,18), (4,18), (5,18),
    (6,18), (7,18), (8,18), (9,18), (10,18), (11,18), (12,18)};
    public List<(int,int)> leftBuilding = new List<(int,int)> {(2,2), (2,3), (2,4), (2,5), (8,2), (8,3), (8,4),
    (8,5), (15,2), (15,3), (15,4), (15,5), (18,2), (18,3), (18,4), (18,5), (2,13), (2,14), (8,13), (8,14),
    (15,13), (15,14), (15,15), (15,16), (15,17), (15,18), (15,19), (15,20), (18,13), (18,14), (18,15), (18,16),
    (18,17), (18,18), (18,19), (18,20), (2,19), (2,20)};
    public List<(int,int)> rightBuilding = new List<(int,int)> {(5,2), (5,3), (5,4), (5,5), (12,2), (12,3),
    (12,4), (12,5), (21,2), (21,3), (21,4), (21,5), (5,13),(5,14), (12,13), (12,14), (21,13), (21,14), 
    (21,15), (21,16), (21,17), (21,18), (21,19), (21,20), (12,19), (12,20)};
    // Start is called before the first frame update
    void Start()
    {
        MakeTiles(layout.text);
    }
void MakeTiles(string tiles)
    {
        int x = 0;
        // Mesa has y 0 at the bottom
        // To draw from the top, find the rows of the file
        // and move down
        // Remove the last enter, and one more to start at 0
        int y = tiles.Split('\n').Length - 2;
        Debug.Log(y);

        Vector3 position;
        GameObject tile;

        for (int i=0; i<tiles.Length; i++) {
            if (tiles[i] == '>' || tiles[i] == '<') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'v' || tiles[i] == '^') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 0, 0));
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'x') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(crossPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'S' || tiles[i] == 's') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                if (upLight.Contains((x,y))){
                    tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 0, 0));
                    tile.transform.parent = transform;
                    tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, 0, 0));
                } else if (downLight.Contains((x,y))){
                    tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 0, 0));
                    tile.transform.parent = transform;
                    tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, 180, 0));
                } else if (leftLight.Contains((x,y))) {
                    tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                    tile.transform.parent = transform;
                    tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, 270, 0));
                } else {
                    tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                    tile.transform.parent = transform;
                    tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, 90, 0));
                }
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'e') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(emptyPrefab, position, Quaternion.Euler(0, 0, 0));
                tile.transform.parent = transform;
                if (upBuilding.Contains((x, y))){
                    tile = Instantiate(parkingPrefab, position, Quaternion.Euler(0, 180, 0));
                } else if(downBuilding.Contains((x, y))){
                    tile = Instantiate(parkingPrefab, position, Quaternion.Euler(0, 0, 0));
                } else if(leftBuilding.Contains((x, y))){
                    tile = Instantiate(parkingPrefab, position, Quaternion.Euler(0, 90, 0));
                } else {
                    tile = Instantiate(parkingPrefab, position, Quaternion.Euler(0, 270, 0));
                }
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '#') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(emptyPrefab, position, Quaternion.Euler(0, 0, 0));
                tile.transform.parent = transform;
                int n = Random.Range(1, 6);
                int degree = 0;
                if (upBuilding.Contains((x, y))){
                    degree = 180;
                } else if(downBuilding.Contains((x, y))){
                    degree = 0;
                } else if(leftBuilding.Contains((x, y))){
                    degree = 90;
                } else {
                    degree = 270;
                }
                switch(n){
                    case 1:
                        // Rota en Z, abajo 90
                        tile = Instantiate(building1Prefab, position, Quaternion.Euler(-90, 0, degree + 90));
                        break;
                    case 2:
                        // Rota en Y, abajo 270
                        tile = Instantiate(building2Prefab, position, Quaternion.Euler(0, degree + 270, 0));
                        break;
                    case 3:
                        // Rota en Y, abajo 270
                        tile = Instantiate(building3Prefab, position, Quaternion.Euler(0, degree + 270, 0));
                        break;
                    case 4:
                        // Rota en Z, abajo 270
                        tile = Instantiate(building4Prefab, position, Quaternion.Euler(-90, 0, degree + 270));
                        break;
                    case 5:
                        // Rota en Y, abajo 0
                        tile = Instantiate(building5Prefab, position, Quaternion.Euler(0, degree, 0));
                        tile.transform.localScale = new Vector3(0.3f, Random.Range(0.07f, 0.2f), 0.3f);
                        break;
                }
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '\n') {
                x = 0;
                y -= 1;
            }
        }

    }
}
