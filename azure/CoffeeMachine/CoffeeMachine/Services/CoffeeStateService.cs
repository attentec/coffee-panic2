using CoffeeMachine.Models;

namespace CoffeeMachine.Services;

public static class CoffeeStateService
{
    static CoffeeState CurrentState;
    static CoffeeStateService()
    {
        CurrentState = new CoffeeState { Weight = 0, Timestamp = 0 };
    }

    public static CoffeeState GetCurrentState() => CurrentState;

    public static void SetCurrentState(CoffeeState state)
    {
        CurrentState = state;
    }
}
