# Auto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**size** | **int** | Volume Size | 
**name** | **str** | Volume Name | [optional] 
**transport** | **str** | Transport Type | [optional] 
**force** | **bool** | Force | [optional] 
**options** | **object** | Options to be configured | [optional] 
**advanced** | **bool** | Allow setting advanced options | [optional] 
**experimental** | **bool** | Allow setting experimental options | [optional] 
**deprecated** | **bool** | Allow setting deprecated options | [optional] 
**metadata** | **object** | Set Volume Metadata | [optional] 
**flags** | **object** | Set Flags | [optional] 
**distribute** | **int** | Distribute count | [optional] 
**replica** | **int** | Replica Count | [optional] 
**arbiter** | **int** | Arbiter Count | [optional] 
**disperse** | **int** | Disperse count | [optional] 
**disperse_redundancy** | **int** | Disperse Redundancy count | [optional] 
**disperse_data** | **int** | Disperse Data count | [optional] 
**snapshot** | **bool** | Enable Snapshot for the Volume | [optional] 
**snapshot_reserve_factor** | **float** | Snapshot reserve factor | [optional] 
**limit_peers** | **list[str]** | Create Volume only from these peers | [optional] 
**limit_zones** | **list[str]** | Create Volume only from these zones | [optional] 
**exclude_peers** | **list[str]** | Do not create Volume from these peers | [optional] 
**exclude_zones** | **list[str]** | Do not create Volume from these zones | [optional] 
**subvolume_zones_overlap** | **bool** | Bricks of different subvolume can be created on same device/peer/zone | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


