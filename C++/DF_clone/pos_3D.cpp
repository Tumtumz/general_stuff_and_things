#include "pos_3D.h"

pos_3D::pos_3D(){
    x = 0;
    y = 0;
    z = 0;
}

pos_3D::pos_3D(int x, int y , int z){
    this->x = x;
    this->y = y;
    this->z = z;
}

std::string pos_3D::to_string(){
    return "pos_3D(" + std::to_string(x) + ", " + std::to_string(y) + ", " + std::to_string(z) + ")";
}

pos_3D pos_3D::add_pos(pos_3D other){
    return pos_3D(this->x + other.x, this->y + other.y, this->z + other.z);
}

pos_3D pos_3D::add_XYZ(int x, int y, int z){
    return pos_3D(this->x + x, this->y + y, this->z + z);
}

bool operator<(pos_3D first, pos_3D second){
    if (first.x != second.x){
        return first.x < second.x;
    }
    else if (first.y != second.y){
        return first.y < second.y;
    }
    else if (first.z != second.z){
        return first.z < second.z;
    }
    else{
        // assert(first == second);
        return false;
    }
}

bool operator==(pos_3D first, pos_3D second){
    return first.x == second.x && first.y == second.y && first.z == second.z;
}

pos_3D operator+(pos_3D first, pos_3D second){
    return pos_3D{first.x + second.x, first.y + second.y, first.z + second.z};
}

