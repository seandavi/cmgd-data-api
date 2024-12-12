# Skaffold

To specify that you don't want to apply an IngressRoute until actual deployment while using Skaffold for development, you can utilize Skaffold's profiles feature and port-forwarding capabilities. Here's how to achieve this:

## Skaffold Configuration

1. Create a separate profile for production in your `skaffold.yaml` file:

```yaml
apiVersion: skaffold/v2beta4
kind: Config

# ... other configurations ...

profiles:
  - name: prod
    deploy:
      kubectl:
        manifests:
          - ./kubernetes-manifests/*.yaml  # Include all manifests, including IngressRoute

# Development configuration (default)
deploy:
  kubectl:
    manifests:
      - ./kubernetes-manifests/*.service.yaml
      - ./kubernetes-manifests/*.deployment.yaml
      # Exclude IngressRoute manifest

portForward:
  - resourceType: service
    resourceName: your-service-name
    namespace: default
    port: 80
    localPort: 8080
```

2. Ensure your IngressRoute is in a separate YAML file, e.g., `ingressroute.yaml`[^1].

## Usage

For development:
- Run `skaffold dev` or `skaffold run` without any profile. This will apply only the service and deployment manifests, and set up port-forwarding[^6].

For production deployment:
- Use `skaffold run -p prod` to apply all manifests, including the IngressRoute[^5].

## Additional Considerations

- Place your IngressRoute configuration in a separate file to easily exclude it during development[^4].
- Utilize Skaffold's automatic port-forwarding for services in development mode[^6].
- You can customize port-forwarding settings in the `portForward` section of your `skaffold.yaml`[^3].

By following this approach, you can effectively use port-forwarding for local development while reserving the IngressRoute for production deployment[^2][^6].

[^1]: https://doc.traefik.io/traefik/v2.2/routing/providers/kubernetes-crd/
[^2]: https://blog.palark.com/intro-to-skaffold-for-easy-kubernetes-development/
[^3]: https://skaffold.dev/docs/port-forwarding/
[^4]: https://docs.rancherdesktop.io/how-to-guides/traefik-ingress-example/
[^5]: https://skaffold.dev/docs/deployers/
[^6]: https://skaffold-staging.web.app/docs/pipeline-stages/port-forwarding/
[^7]: https://stackoverflow.com/questions/64897332/kubernetes-ingress-skaffold-documentation
[^8]: https://dev.to/ksaaskil/how-to-deploy-django-on-kubernetes-with-skaffold-for-development-and-production-3kp9