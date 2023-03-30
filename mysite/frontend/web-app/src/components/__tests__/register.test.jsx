import {render, screen, cleanup} from "@testing-library/react";
import LoginPage from "../../pages/LoginPage";
import Register from "../../pages/Register";
import { BrowserRouter as Router } from "react-router-dom";


test('renders link to login button', () => {
    render(<Router><Register/></Router>);
    const registerLink = screen.getByTestId("link-button");
    expect(registerLink).toBeInTheDocument();
})

test('renders input boxes', () => {
    render(<Router><Register/></Router>);
    const inputBoxes = screen.getAllByTestId("input-boxes");
    expect(inputBoxes.length).toBe(7);
}) 


test('input boxes should be empty', () => {
    render(<Router><Register/></Router>);

    const userNameInput = screen.getByPlaceholderText(/Username/i);
    const firstNameInput = screen.getByPlaceholderText(/First Name/i);
    const lastNameInput = screen.getByPlaceholderText(/Last Name/i);
    const emailInput = screen.getByPlaceholderText(/example@email.com/i);
    const phoneInput = screen.getByPlaceholderText(/Enter phone number/i);
    const passInput = document.getElementById("password");
    const secondPassInput = document.getElementById("password-confirmed");
   
    
    expect(userNameInput.value).toBe("");
    expect(firstNameInput.value).toBe("");
    expect(lastNameInput.value).toBe("");
    expect(emailInput.value).toBe("");
    expect(phoneInput.value).toBe("");
    expect(passInput.value).toBe("");
    expect(secondPassInput.value).toBe("");
    
})








