package main

import (
	"errors"
	"fmt"
)

// MyInterface is an example interface with a method returning an error.
type MyInterface interface {
	DoSomething() error
}

// MyStruct implements the MyInterface interface.
type MyStruct struct{}

// DoSomething returns an error indicating an issue.
func (ms *MyStruct) DoSomething() error {
	// Simulate an error condition
	return errors.New("something went wrong")
}

func main() {
	var myInstance MyInterface = &MyStruct{}
	err := myInstance.DoSomething()

	if err != nil {
		fmt.Println("Error:", err.Error())
	} else {
		fmt.Println("Operation succeeded")
	}
}
