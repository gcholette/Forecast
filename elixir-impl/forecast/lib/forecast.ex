import Forecast.File
import HTTPoison
import ExGrib
alias ExGrib.Grib2, as: Grib2

defmodule Forecast do
  def loadData do
    url =
      "https://dd.weather.gc.ca/model_hrdps/east/grib2/18/003/CMC_hrdps_east_TMP_TGL_2_ps2.5km_2022041618_P003-00.grib2"

    case HTTPoison.get(url) do
      {:ok, %HTTPoison.Response{status_code: 200, body: body}} ->
        trimmedBody = binary_part(binary_part(body, 16, byte_size(body) - 16), 0, 21)
        IO.inspect(trimmedBody, binaries: :as_binaries, limit: 1000)

        case Grib2.parse_all(body) do
          {:ok, section, _} -> IO.inspect(section)
          :error -> IO.puts('Nuh')
        end

      {:ok, %HTTPoison.Response{status_code: 404}} ->
        IO.puts("Not found :(")

      {:error, %HTTPoison.Error{reason: reason}} ->
        IO.inspect(reason)
    end

    # {:ok, section, _} = Grib2.identification(data)
  end
end
