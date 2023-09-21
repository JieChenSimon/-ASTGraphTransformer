pragma solidity ^0.8.9;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 * @custom:dev-run-script ./scripts/deploy_with_ethers.ts
 */
contract SubtractionContract {
    uint256 public variable1;
    uint256 public variable2;
    uint256 public variable3;
    uint256 public tmp;
    
    constructor(uint256 _initialValue1, uint256 _initialValue2) {
        variable1 = _initialValue1;
        variable2 = _initialValue2;
    }

    function subtract() public {
        require(variable1 >= variable2, "Variable1 must be greater than or equal to Variable2");
        tmp = variable1 - variable2 - variable3;
    }
}