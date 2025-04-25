USE [Crash Scope DWH]
GO

/****** Object:  Table [dbo].[Dim_Vehicles]    Script Date: 4/24/2025 3:21:56 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Dim_Vehicles](
	[VEHICLE_ID_PK_SK] [int] IDENTITY(1,1) NOT NULL,
	[VEHICLE_ID_BK] [int] NULL,
	[Crash_Unit_ID_BK] [int] NULL,
	[Unit_Type] [nvarchar](50) NULL,
	[Make] [nvarchar](100) NULL,
	[Model] [nvarchar](100) NULL,
	[Lic_Plate_State] [nvarchar](50) NULL,
	[Vehicle_Year] [int] NULL,
	[Vehicle_Defect] [nvarchar](50) NULL,
	[Vehicle_Type] [nvarchar](100) NULL,
	[Vehicle_Use] [nvarchar](100) NULL,
	[Travel_direction] [nvarchar](50) NULL,
	[maneuver] [nvarchar](100) NULL,
	[Occupant_CNT] [int] NULL,
	[First_contact_point] [nvarchar](100) NULL,
	[Unit_No] [int] NULL,
	[SSC] [int] NULL,
	[start_date] [datetime] NULL,
	[end_date] [datetime] NULL,
	[is_current] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[VEHICLE_ID_PK_SK] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Dim_Vehicles] ADD  DEFAULT (getdate()) FOR [start_date]
GO

ALTER TABLE [dbo].[Dim_Vehicles] ADD  DEFAULT ((1)) FOR [is_current]
GO


