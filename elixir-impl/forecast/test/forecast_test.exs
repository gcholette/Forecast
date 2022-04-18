defmodule ForecastTest do
  use ExUnit.Case
  doctest Forecast

  test "greets the world" do
    assert Forecast.hello() == :world
  end
end
