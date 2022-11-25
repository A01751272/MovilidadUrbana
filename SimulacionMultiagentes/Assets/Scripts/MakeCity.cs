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
    int tileSize = 1;

    //Listas con coordenadas para prefabs especificos
    public List<(int,int)> upLight = new List<(int,int)> {(0,13), (1,13), (6,2), (7,2), (13,2), (14,2)};
    public List<(int,int)> downLight = new List<(int,int)> {(6,16), (7,16), (22, 7), (23, 7), (16,22), (17,22)};
    public List<(int,int)> leftLight = new List<(int,int)> {(5,0), (5,1), (12,0), (12,1), (21,9), (21,8)};
    public List<(int,int)> rightLight = new List<(int,int)> {(2,12), (2,11), (8,18), (8,17), (18,23), (18,24)};
    public List<(int,int)> upBuilding = new List<(int,int)> {(2,7), (3,7), (4,7), (5,7), (8,7), (9,7), (10,7), 
    (11,7), (12,7), (15,7), (18,7), (19,7), (20,7), (21,7), (2,10), (3,10), (4,10), (5,10), (6,10), (7,10), (8,10),
    (10,10), (11,10), (14,10), (15,10), (16,10), (19,10), (20,10), (21,10), (2,16), (3,16), (4,16), (5,16), (8,16),
    (9,16), (10,16), (11,16), (12,16), (2,22), (3,22), (4,22), (5,22), (6,22), (7,22), (8,22), (9,22), (10,22),
    (11,22), (12,22), (15,22), (18,22), (19,22), (20,22), (21,22)};
    public List<(int,int)> downBuilding = new List<(int,int)> {(2,2), (3,2), (4,2), (5,2), (8,2), (9,2), (10,2),
    (11,2), (12,2), (15,2), (18,2), (19,2), (20,2), (21,2), (2, 13), (3,13), (4,13), (5,13),(8,13), (9,13), 
    (10,13), (11,13), (12,13), (15,13), (18,13), (19,13), (20,13), (21,13), (2,19), (3,19), (4,19), (5,19),
    (6,19), (7,19), (8,19), (9,19), (10,19), (11,19), (12,19)};
    public List<(int,int)> leftBuilding = new List<(int,int)> {(2,3), (2,4), (2,5), (2,6), (8,3), (8,4), (8,5),
    (8,6), (15,3), (15,4), (15,5), (15,6), (18,3), (18,4), (18,5), (18,6), (2,14), (2,15), (8,14), (8,15),
    (15,14), (15,15), (15,16), (15,17), (15,18), (15,19), (15,20), (15,21), (18,14), (18,15), (18,16), (18,17),
    (18,18), (18,19), (18,20), (18,21), (2,20), (2,21)};
    public List<(int,int)> rightBuilding = new List<(int,int)> {(5,3), (5,4), (5,5), (5,6), (12,3), (12,4),
    (12,5), (12,6), (21,3), (21,4), (21,5), (21,6), (5,14),(5,15), (12,14), (12,15), (21,14), (21,15), 
    (21,16), (21,17), (21,18), (21,19), (21,20), (21,21), (12,20), (12,21)};

    public List<(int, int)> upRightCorner = new List<(int, int)> {(22,23),(23,24)};
    public List<(int, int)> upLeftCorner = new List<(int, int)> {(0,24),(1,23)};
    public List<(int, int)> bottomRightCorner = new List<(int, int)> {(23,0),(22,1)};
    public List<(int, int)> bottomLeftCorner = new List<(int, int)> {(0,0),(1,1)};
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
        int y = tiles.Split('\n').Length - 1;

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
                if(upRightCorner.Contains((x,y))){
                    tile = Instantiate(curvePrefab, position, Quaternion.Euler(0, 0, 0));
                } else if (upLeftCorner.Contains((x,y))){
                    tile = Instantiate(curvePrefab, position, Quaternion.Euler(0, 270, 0));
                } else if (bottomRightCorner.Contains((x,y))){
                    tile = Instantiate(curvePrefab, position, Quaternion.Euler(0, 90, 0));
                } else if (bottomLeftCorner.Contains((x,y))){
                    tile = Instantiate(curvePrefab, position, Quaternion.Euler(0, 180, 0));
                } else {
                    tile = Instantiate(crossPrefab, position, Quaternion.Euler(0, 90, 0));
                }
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
