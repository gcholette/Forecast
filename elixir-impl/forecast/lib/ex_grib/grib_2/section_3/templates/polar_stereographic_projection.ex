defmodule ExGrib.Grib2.Section3.Templates.PolarStereographicProjection do
  @moduledoc """
  Template 3.20

  Polar stereographic projection

  https://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_temp3-20.shtml
  """
  alias ExGrib.Grib2.Section3.ScanningMode
  alias ExGrib.Grib2.Section3.ShapeOfReferenceSystem, as: ShapeOfTheEarth

  defstruct shape_of_the_earth: nil,
            radius_scale_factor: nil,
            radius_scale_value: nil,
            major_axis_scale_factor: nil,
            major_axis_scale_value: nil,
            minor_axis_scale_factor: nil,
            minor_axis_scale_value: nil,
            n_x: nil,
            n_y: nil,
            la1: nil,
            lo1: nil,
            resolution: nil,
            lad: nil,
            lov: nil,
            dx: nil,
            dy: nil,
            projection_centre_flag: nil,
            scanning_mode: nil

  @type input :: binary()
  @type t() :: {:ok, %__MODULE__{}, binary()} | :error

  @spec get(input()) :: t()
  def get(<<
        # 15 - Shape of the Earth (See Code Table 3.2)
        shape_of_the_earth::integer(),
        # 16 - Scale Factor of radius of spherical Earth
        radius_scale_factor::integer(),
        # 17-20 Scale value of radius of spherical Earth
        radius_scale_value::integer-size(32),
        # 21 Scale factor of major axis of oblate spheroid Earth
        major_axis_scale_factor::integer(),
        # 22-25 Scaled value of major axis of oblate spheroid Earth
        major_axis_scale_value::integer-size(32),
        # 26 Scale factor of minor axis of oblate spheroid Earth
        minor_axis_scale_factor::integer(),
        # 27-30 Scaled value of minor axis of oblate spheroid Earth
        minor_axis_scale_value::integer-size(32),
        n_x::integer-size(32),
        n_y::integer-size(32),
        la1::integer-size(32),
        lo1::integer-size(32),
        resolution::integer(),
        lad::integer-size(32),
        lov::integer-size(32),
        dx::integer-size(32),
        dy::integer-size(32),
        projection_centre_flag::integer(),
        # 72 Scanning mode (flags — see Flag Table 3.4 and Note 6)
        scanning_mode::integer()
      >>) do
    template = %__MODULE__{
      shape_of_the_earth: ShapeOfTheEarth.get(shape_of_the_earth),
      radius_scale_factor: radius_scale_factor,
      radius_scale_value: radius_scale_value,
      major_axis_scale_factor: major_axis_scale_factor,
      major_axis_scale_value: major_axis_scale_value,
      minor_axis_scale_factor: minor_axis_scale_factor,
      minor_axis_scale_value: minor_axis_scale_value,
      n_x: n_x,
      n_y: n_y,
      la1: la1,
      lo1: lo1,
      resolution: resolution,
      lad: lad,
      lov: lov,
      dx: dx,
      dy: dy,
      projection_centre_flag: projection_centre_flag,
      scanning_mode: ScanningMode.get(scanning_mode)
    }

    {:ok, template, <<>>}
  end

  def get(_), do: :error
end
