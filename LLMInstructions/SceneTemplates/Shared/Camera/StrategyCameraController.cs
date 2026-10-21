using UnityEngine;
using UnityEngine.InputSystem;

namespace UnityStarter.SceneTemplates
{
    /// <summary>
    /// Standalone strategy camera. Owns a private input instance; the host can block navigation
    /// when UI or tools own input. Distances are world units and angles are degrees.
    /// </summary>
    [DisallowMultipleComponent]
    public sealed class StrategyCameraController : MonoBehaviour
    {
        private const string k_mapName = "Camera";
        [Header("Rig")]
        [SerializeField] private Transform m_pitchPivot;
        [SerializeField] private Camera m_lens;
        [Tooltip("Shared source definition; each rig owns a private runtime copy.")]
        [SerializeField] private InputActionAsset m_inputDefinition;
        [Header("Navigation")]
        [SerializeField, Min(0.1f)] private float m_panSpeed = 25f;
        [SerializeField, Min(1f)] private float m_sprintMultiplier = 3f;
        [SerializeField, Min(0f)] private float m_rotationSpeed = 100f;
        [Tooltip("Yaw degrees per pointer pixel while the middle mouse button is held.")]
        [SerializeField, Min(0f)] private float m_dragSensitivity = 0.15f;
        [SerializeField, Min(0.01f)] private float m_zoomSensitivity = 8f;
        [SerializeField, Min(0f)] private float m_smoothingTime = 0.12f;
        [Header("View")]
        [SerializeField, Min(0.1f)] private float m_minDistance = 12f;
        [SerializeField, Min(0.1f)] private float m_maxDistance = 120f;
        [SerializeField, Min(0.1f)] private float m_startDistance = 55f;
        [SerializeField, Range(15f, 80f)] private float m_closePitch = 35f;
        [SerializeField, Range(15f, 80f)] private float m_farPitch = 65f;
        [SerializeField, Range(15f, 80f)] private float m_orthographicPitch = 45f;
        [SerializeField] private bool m_isOrthographic;
        private InputActionAsset m_inputInstance;
        private InputActionMap m_map;
        private InputAction m_pan;
        private InputAction m_rotate;
        private InputAction m_zoom;
        private InputAction m_drag;
        private InputAction m_look;
        private InputAction m_sprint;
        private InputAction m_toggleProjection;
        private Vector3 m_targetPosition;
        private Vector3 m_positionVelocity;
        private float m_targetYaw;
        private float m_yawVelocity;
        private float m_distance;
        private float m_targetDistance;
        private float m_zoomVelocity;
        private bool m_isInputBlocked;
        private bool m_hasFocus = true;

        /// <summary>Whether navigation is blocked by the host UI or a construction tool.</summary>
        public bool IsInputBlocked => m_isInputBlocked;
        /// <summary>Whether the lens uses the fixed-tilt orthographic view.</summary>
        public bool IsOrthographic => m_isOrthographic;
        /// <summary>Whether this rig currently owns a middle-mouse camera drag.</summary>
        public bool IsDragging => !m_isInputBlocked && m_hasFocus && m_drag != null && m_drag.IsPressed();

        private void Awake()
        {
            if (m_pitchPivot == null || m_lens == null || m_inputDefinition == null)
            {
                Debug.LogError("Strategy camera requires a pitch pivot, lens, and input definition.", this);
                enabled = false;
                return;
            }

            // Enabling one rig must never enable or disable another rig's shared source actions.
            m_inputInstance = Instantiate(m_inputDefinition);
            m_map = m_inputInstance.FindActionMap(k_mapName, true);
            m_pan = m_map.FindAction("Pan", true);
            m_rotate = m_map.FindAction("Rotate", true);
            m_zoom = m_map.FindAction("Zoom", true);
            m_drag = m_map.FindAction("Drag", true);
            m_look = m_map.FindAction("Look", true);
            m_sprint = m_map.FindAction("Sprint", true);
            m_toggleProjection = m_map.FindAction("ToggleProjection", true);
            m_distance = Mathf.Clamp(m_startDistance, m_minDistance, m_maxDistance);
            m_targetDistance = m_distance;
            SynchronizePose();
            ApplyLens();
        }

        private void OnEnable()
        {
            SynchronizePose();
            m_map?.Enable();
        }

        private void OnDisable()
        {
            m_map?.Disable();
            SynchronizePose();
        }

        private void OnDestroy()
        {
            if (m_inputInstance != null)
            {
                m_inputInstance.Disable();
                Destroy(m_inputInstance);
            }
        }

        private void Update()
        {
            if (m_map == null)
            {
                return;
            }

            float deltaTime = Time.unscaledDeltaTime;
            if (!m_isInputBlocked && m_hasFocus)
            {
                ReadNavigation(deltaTime);
            }

            transform.position = Vector3.SmoothDamp(transform.position, m_targetPosition,
                ref m_positionVelocity, m_smoothingTime, Mathf.Infinity, deltaTime);
            float yaw = Mathf.SmoothDampAngle(transform.eulerAngles.y, m_targetYaw,
                ref m_yawVelocity, m_smoothingTime, Mathf.Infinity, deltaTime);
            transform.rotation = Quaternion.Euler(0f, yaw, 0f);
            m_distance = Mathf.SmoothDamp(m_distance, m_targetDistance,
                ref m_zoomVelocity, m_smoothingTime, Mathf.Infinity, deltaTime);
            ApplyLens();
        }

        private void OnApplicationFocus(bool hasFocus)
        {
            m_hasFocus = hasFocus;
            if (!hasFocus)
            {
                SynchronizePose();
            }
        }

        private void OnValidate()
        {
            m_minDistance = Mathf.Max(0.1f, m_minDistance);
            m_maxDistance = Mathf.Max(m_minDistance, m_maxDistance);
            m_startDistance = Mathf.Clamp(m_startDistance, m_minDistance, m_maxDistance);
        }

        /// <summary>Blocks new navigation and cancels pending camera movement when true.</summary>
        public void SetInputBlocked(bool isBlocked)
        {
            m_isInputBlocked = isBlocked;
            if (isBlocked)
            {
                SynchronizePose();
            }
        }

        /// <summary>Changes projection while keeping the rig's ground focus and current zoom scale.</summary>
        public void SetOrthographic(bool isOrthographic)
        {
            m_isOrthographic = isOrthographic;
            ApplyLens();
        }

        private void ReadNavigation(float deltaTime)
        {
            float sprint = m_sprint.IsPressed() ? m_sprintMultiplier : 1f;
            Vector2 pan = Vector2.ClampMagnitude(m_pan.ReadValue<Vector2>(), 1f);
            float zoomScale = Mathf.Max(1f, m_distance / m_startDistance);
            m_targetPosition += transform.TransformDirection(new Vector3(pan.x, 0f, pan.y))
                * (m_panSpeed * zoomScale * sprint * deltaTime);
            m_targetYaw += m_rotate.ReadValue<float>() * m_rotationSpeed * deltaTime;
            if (IsDragging)
            {
                m_targetYaw += m_look.ReadValue<Vector2>().x * m_dragSensitivity;
            }

            // Wheel events are deltas, so they must not be multiplied by frame duration.
            float scroll = Mathf.Clamp(m_zoom.ReadValue<float>(), -1f, 1f);
            m_targetDistance = Mathf.Clamp(m_targetDistance - scroll * m_zoomSensitivity * zoomScale * sprint,
                m_minDistance, m_maxDistance);
            if (m_toggleProjection.WasPressedThisFrame())
            {
                SetOrthographic(!m_isOrthographic);
            }
        }

        private void SynchronizePose()
        {
            m_targetPosition = transform.position;
            m_targetYaw = transform.eulerAngles.y;
            m_targetDistance = m_distance;
            m_positionVelocity = Vector3.zero;
            m_yawVelocity = 0f;
            m_zoomVelocity = 0f;
        }

        private void ApplyLens()
        {
            if (m_lens == null || m_pitchPivot == null)
            {
                return;
            }

            float zoom = Mathf.InverseLerp(m_minDistance, m_maxDistance, m_distance);
            float pitch = m_isOrthographic ? m_orthographicPitch : Mathf.Lerp(m_closePitch, m_farPitch, zoom);
            m_pitchPivot.localRotation = Quaternion.Euler(pitch, 0f, 0f);
            m_lens.transform.localPosition = new Vector3(0f, 0f, -m_distance);
            m_lens.orthographic = m_isOrthographic;
            m_lens.orthographicSize = m_distance * Mathf.Tan(m_lens.fieldOfView * 0.5f * Mathf.Deg2Rad);
        }
    }
}
