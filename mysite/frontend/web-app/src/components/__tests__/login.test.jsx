import {render, screen, cleanup, fireEvent} from "@testing-library/react";
import LoginPage from "../../pages/LoginPage";
import { BrowserRouter as Router } from "react-router-dom";

test('renders link to login button', () => {
    render(<Router><LoginPage/></Router>);
    const registerLink = screen.getByTestId("link-button");
    expect(registerLink).toBeInTheDocument();
})

test('username input should be rendered', () => {
    render(<Router><LoginPage/></Router>);
    const userNameInput = screen.getByPlaceholderText(/username/i);
    expect(userNameInput).toBeInTheDocument();
})

test('password input should be rendered', () => {
    render(<Router><LoginPage/></Router>);
    const passInput = screen.getByPlaceholderText(/password/i);
    expect(passInput).toBeInTheDocument();
})

test('button input should be rendered', () => {
    render(<Router><LoginPage/></Router>);
    const buttonInput = screen.getByRole('button');
    expect(buttonInput).toBeInTheDocument();
})

test('username input should be empty', () => {
    render(<Router><LoginPage/></Router>);
    const userNameInput = screen.getByPlaceholderText(/username/i);;
    expect(userNameInput.value).toBe("");
})

test('password input should be empty', () => {
    render(<Router><LoginPage/></Router>);
    const passInput = screen.getByPlaceholderText(/password/i);;
    expect(passInput.value).toBe("");
})


test('username input should change', () => {
    render(<Router><LoginPage/></Router>);
    
    const userNameInput = screen.getByPlaceholderText(/username/i);
    const testValue = "test";
    fireEvent.change(userNameInput, {target:{value:testValue}});
    expect(userNameInput.value).toBe(testValue);
})


test('password input should be empty', () => {
    render(<Router><LoginPage/></Router>);
    const passInput = screen.getByPlaceholderText(/password/i);
    const testValue = "test";
    fireEvent.change(passInput, {target:{value:testValue}});
    expect(passInput.value).toBe(testValue);
})


